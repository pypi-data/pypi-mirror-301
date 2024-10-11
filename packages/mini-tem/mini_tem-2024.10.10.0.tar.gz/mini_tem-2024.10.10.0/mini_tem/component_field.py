import dataclasses
from typing import Callable


@dataclasses.dataclass
class ComponentField:
    """
    name, value, unit, on_change
    """
    name: str
    value: float
    unit: str
    on_change: Callable[[float], None]
