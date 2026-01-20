from enum import Enum
from typing import Iterable
from wpilib import AddressableLED as AddressableLED, Color
from wpimath.units import meters as meters, meters_per_second as meters_per_second, meters_per_second_squared as meters_per_second_squared

class PatternState(Enum):
    fill = (0,)
    empty = 1

class FallingSand:
    def __init__(self, colors: Iterable[Color], bar_size: int, led_spacing: meters, intake_velocity: meters_per_second, exit_acceleration: meters_per_second_squared, fill_size: int, gamma: float) -> None: ...
    def reset(self) -> None: ...
