from enum import Enum
from typing import Iterable
from wpilib import AddressableLED as AddressableLED, Color
from wpimath.units import meters_per_second as meters_per_second

class PatternState(Enum):
    fill = (0,)
    empty = 1

class ColorStack:
    def __init__(self, colors: Iterable[Color], bar_size: int, velocity: meters_per_second, fill_size: int, empty_size: int, gamma: float) -> None: ...
    def reset(self) -> None: ...
