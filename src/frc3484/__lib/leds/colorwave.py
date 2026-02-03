from wpilib import AddressableLED, Color, Timer
from wpimath.units import meters, meters_per_second
import math
from typing import Iterable

class ColorWave :
    def __init__(self, colors: Iterable[Color], led_spacing: meters, wavelength: meters, gamma: float, velocity: meters_per_second, bar_size: int) -> None:
        self._colors: list[Color] = [color for color in colors]
        self._bar_size: int = bar_size
        self._wavelength = wavelength
        self._gamma = gamma
        self._velocity = velocity / led_spacing
        self._timer = Timer()
    def _apply_to(self, data: list[AddressableLED.LEDData]):
        for i in range(len(data)):
            data[i].setLED(self._apply_brightness(self._colors[self._get_color_index(i)], self._get_brightness(i)))
        return data
    def _get_brightness(self, offset: int):
        return (1 - math.cos(2 * math.pi / self._wavelength) * (offset - self._wave_position())) / 2
    def _apply_brightness(self, color: Color, brightness: float) -> Color:
        return Color(self._gamma_correction(color.red * brightness), self._gamma_correction(color.green * brightness), self._gamma_correction(color.blue * brightness) )
    def _get_color_index(self, offset: int) -> int:
        return (offset // self._bar_size) % len(self._colors) 
    def  _positive_fmod(self, numerator: float, denominator: float)-> float:
        return ((numerator % denominator) + denominator % denominator)
    def _gamma_correction(self, brightness: float) -> float:
        return brightness ** self._gamma
    def _wave_position(self):
        return self._timer.get() * self._velocity