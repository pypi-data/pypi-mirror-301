from __future__ import annotations

import attrs
import cattrs


@attrs.define
class MyType:
    value: dict[str, int]


r = cattrs.unstructure(MyType({"a": 1, "b": 2}), MyType)
print(r)
# cattrs.register_structure_hook(MyType.__value__, structure_hook_dict)
