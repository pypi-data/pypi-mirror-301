import contextlib
import operator
import pickle
from collections.abc import Callable, Iterator
from typing import TypeAlias, Literal
from typing import (
    TypeVar,
    LiteralString,
    Any,
)

import anyio
import attrs
import trio
from anyio.streams.buffered import BufferedByteReceiveStream

from ._prefix_size import receive_with_size_prefix, send_with_size_prefix
from ._server import (
    CallRequest,
    ReturnValue,
    CallResponse,
    CallResponseSuccess,
    CallResponseFailure,
    DeleteProxyRequest,
    TerminateRequest,
    RemoteError,
    RemoteCallError,
)
from .._async_converter import AsyncConverter
from .._proxy import Proxy

T = TypeVar("T")

ReturnedType: TypeAlias = Literal["copy", "proxy"]


@contextlib.contextmanager
def unwrap_remote_error_cm():
    try:
        yield
    except RemoteCallError as remote:
        if original := remote.__cause__:
            # Here we need to break the circle of exceptions.
            # Indeed, original.__context__ is now remote, and remote.__cause__ is
            # original.
            # If not handled, this would cause recursion issues when anything tries
            # to handle the exception down the line.
            remote.__cause__ = None
            raise original from None
        else:
            raise


@attrs.frozen
class MethodCaller:
    method: LiteralString

    def __call__(self, obj: Any, *args: Any, **kwargs: Any) -> Any:
        return getattr(obj, self.method)(*args, **kwargs)

    def __str__(self):
        return f"call method {self.method}"


class RPCClient(AsyncConverter):
    def __init__(self, host: str, port: int):
        self._host = host
        self._port = port

        self._exit_stack = contextlib.AsyncExitStack()

        self._request_id = 0

    async def __aenter__(self):
        await self._exit_stack.__aenter__()
        self._stream = await anyio.connect_tcp(self._host, self._port)
        self._receive_stream = BufferedByteReceiveStream(self._stream)
        await self._exit_stack.enter_async_context(self._stream)
        self._exit_stack.push_async_callback(self.terminate)
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        with anyio.CancelScope(shield=True):
            await self._exit_stack.__aexit__(exc_type, exc_value, traceback)

    async def call(self, fun: Callable[..., T], *args, **kwargs) -> T:
        with unwrap_remote_error_cm():
            return await self._call(fun, *args, **kwargs)

    async def _call(
        self,
        fun: Callable[..., T],
        *args: Any,
        **kwargs: Any,
    ) -> T:
        request = self._build_request(fun, args, kwargs, "copy")
        pickled = pickle.dumps(request)
        await send_with_size_prefix(self._stream, pickled)

        # We shield the reception from cancellation, otherwise if a cancellation
        # occurs between the send and the receive, the received answer will stay
        # in the buffer as the next answer to read.
        with anyio.CancelScope(shield=True):
            bytes_response = await receive_with_size_prefix(self._receive_stream)
        response = pickle.loads(bytes_response)
        _ensure_response_match_request(response, request)
        return self._build_result(response)

    async def call_method(
        self, obj: Any, method: LiteralString, *args: Any, **kwargs: Any
    ) -> Any:
        with unwrap_remote_error_cm():
            return await self._call_method(obj, method, *args, **kwargs)

    async def _call_method(
        self,
        obj: Any,
        method: LiteralString,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        return await self._call(
            MethodCaller(method=method),
            obj,
            *args,
            **kwargs,
        )

    async def terminate(self):
        request = TerminateRequest()
        pickled_request = pickle.dumps(request)
        await send_with_size_prefix(self._stream, pickled_request)

    @contextlib.asynccontextmanager
    async def call_method_proxy_result(
        self,
        obj: Any,
        method: LiteralString,
        *args: Any,
        **kwargs: Any,
    ):
        caller = operator.methodcaller(method, *args, **kwargs)
        async with self.call_proxy_result(caller, obj) as result:
            yield result

    async def get_attribute(self, obj: Any, attribute: LiteralString) -> Any:
        caller = operator.attrgetter(attribute)
        return await self.call(caller, obj)

    @contextlib.asynccontextmanager
    async def call_proxy_result(self, fun: Callable[..., T], *args: Any, **kwargs: Any):
        request = self._build_request(fun, args, kwargs, "proxy")
        pickled_request = pickle.dumps(request)

        await send_with_size_prefix(self._stream, pickled_request)
        with anyio.CancelScope(shield=True):
            pickled_response = await receive_with_size_prefix(self._receive_stream)
        response = pickle.loads(pickled_response)
        _ensure_response_match_request(response, request)

        with unwrap_remote_error_cm():
            proxy = self._build_result(response)
        assert isinstance(proxy, Proxy)
        try:
            yield proxy
        finally:
            await self._close_proxy(proxy)

    @contextlib.asynccontextmanager
    async def _call_proxy_result(
        self, fun: Callable[..., T], *args: Any, **kwargs: Any
    ):
        request = self._build_request(fun, args, kwargs, "proxy")
        pickled_request = pickle.dumps(request)

        await send_with_size_prefix(self._stream, pickled_request)
        with anyio.CancelScope(shield=True):
            pickled_response = await receive_with_size_prefix(self._receive_stream)
        response = pickle.loads(pickled_response)
        _ensure_response_match_request(response, request)

        proxy = self._build_result(response)
        assert isinstance(proxy, Proxy)
        try:
            yield proxy
        finally:
            await self._close_proxy(proxy)

    @contextlib.asynccontextmanager
    async def async_context_manager(
        self, cm_proxy: Proxy[contextlib.AbstractContextManager[T]]
    ):
        async with self.call_method_proxy_result(cm_proxy, "__enter__") as result_proxy:
            exception = None
            try:
                yield result_proxy
            except BaseException as e:
                exception = e
        if exception is None:
            exc_type = exc_value = exc_tb = None
        else:
            # We can't pickle trio cancelled error, so we replace it with our own
            reraised = replace_trio_cancelled(exception)
            exc_type = type(reraised)
            exc_value = reraised
            exc_tb = exception.__traceback__

        with anyio.CancelScope(shield=True):
            ignore_exception = await self.call_method(
                cm_proxy, "__exit__", exc_type, exc_value, exc_tb
            )
        if exception is not None and not ignore_exception:
            raise exception

    async def async_iterator(self, proxy: Proxy[Iterator[T]]):
        while True:
            try:
                value = await self._call_method(proxy, "__next__")
            except RemoteError as error:
                if isinstance(error.__cause__, StopIteration):
                    break
                else:
                    with unwrap_remote_error_cm():
                        raise
            else:
                yield value

    async def _close_proxy(self, proxy: Proxy[T]) -> None:
        request = DeleteProxyRequest(id_=self._request_id, proxy=proxy)
        self._request_id += 1
        pickled_request = pickle.dumps(request)
        with anyio.CancelScope(shield=True):
            await send_with_size_prefix(self._stream, pickled_request)

    def _build_request(
        self,
        fun: Callable[..., T],
        args: Any,
        kwargs: Any,
        returned_value: ReturnedType,
    ) -> CallRequest:
        request = CallRequest(
            id_=self._request_id,
            function=fun,
            args=args,
            kwargs=kwargs,
            return_value=(
                ReturnValue.SERIALIZED
                if returned_value == "copy"
                else ReturnValue.PROXY
            ),
        )
        self._request_id += 1
        return request

    @staticmethod
    def _build_result(response: CallResponse) -> Any:
        match response:
            case CallResponseSuccess(result=result):
                return result
            case CallResponseFailure(error=error):
                raise error


class Cancelled(BaseException):
    pass


def _ensure_response_match_request(response, request: CallRequest):
    if not isinstance(response, CallResponse):
        raise ValueError(f"Unexpected response: {response}")
    if not response.id_ == request.id_:
        raise ValueError(
            f"Unexpected response id: {response.id_} instead of {request.id_}"
        )


def replace_trio_cancelled(exception) -> BaseException:
    if exception.__cause__:
        cause = replace_trio_cancelled(exception.__cause__)
    else:
        cause = None
    if exception.__context__:
        context = replace_trio_cancelled(exception.__context__)
    else:
        context = None
    if isinstance(exception, trio.Cancelled):
        new_exception = Cancelled()
    elif isinstance(exception, BaseExceptionGroup):
        new_exception = type(exception)(
            str(exception), [replace_trio_cancelled(e) for e in exception.exceptions]
        )
    else:
        new_exception = type(exception)(str(exception))
    new_exception.__cause__ = cause
    new_exception.__context__ = context
    return new_exception
