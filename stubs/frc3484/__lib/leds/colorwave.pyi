from typing import Iterable
from wpilib import AddressableLED as AddressableLED, Color
from wpimath.units import meters as meters, meters_per_second as meters_per_second

class ColorWave:
    def __init__(self, colors: Iterable[Color], led_spacing: meters, wavelength: meters, gamma: float, velocity: meters_per_second, bar_size: int) -> None: ...
