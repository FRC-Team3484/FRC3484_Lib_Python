from wpilib import AddressableLED, LEDPattern, Color
from wpimath.units import meters, meters_per_second, meters_per_second_squared
from typing import Iterable, List

from enum import Enum

class PatternState(Enum):
    fill = 0,
    empty = 1

class FallingSand:
    def __init__(self, colors: Iterable[Color], bar_size: meters, led_spacing: meters, intake_velocity: meters_per_second, exit_acceleration: meters_per_second_squared, fill_size: int, gamma: float) -> None:
        self._colors: List[Color] = []
        for color in colors:
            self._colors.append(self._correct_gamma(color))
        self._bar_size: meters = bar_size
        self._led_spacing: meters = led_spacing
        self._intake_velocity: meters_per_second = intake_velocity
        self._exit_acceleration: meters_per_second_squared = exit_acceleration
        self._fill_size: int = fill_size
        self._gamma: float = gamma
        self._state: PatternState = PatternState.fill
        self._leds_placed: int = 0
        self._falling_led_position: float = 0.0
        self.reset()

    def reset(self):
        self._leds_placed = 0
        self._falling_led_position = 0.0
        self._state = PatternState.fill

    def _apply_to(self, data: List[AddressableLED.LEDData]):
        match self._state: 
            case PatternState.fill:
                pass


    def _correct_gamma(self, color: Color) -> Color:
        pass