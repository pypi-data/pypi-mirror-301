from typing import reveal_type

from caqtus.types.units import Quantity, ureg, Unit
import pint


if __name__ == "__main__":
    q = Quantity(1, "m")
    print(type(q.magnitude))
    units = Quantity(1, "m").units
    print(type(units))
    print(type(1 * units))
