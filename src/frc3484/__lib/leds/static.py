from wpilib import AddressableLED, LEDPattern, Timer, Color
from wpimath.units import meters
from typing import Iterable
from enum import Enum

class PatternState(Enum):
    fill = 0,
    empty = 1

class Static:
    def __init__(self, colors: Iterable[Color], bar_size: int, led_spacing: meters, fill_size: int, gamma: float, move_rate: int = 0.05) -> None:
        self._colors: list[Color] = []
        for color in colors:
            self._colors.append(self._correct_gamma(color))
        self._bar_size: int = bar_size
        self._led_spacing: meters = led_spacing
        self._fill_size: int = fill_size
        self._gamma: float = gamma
        self._move_rate: int = move_rate
        self._center_point: int
        self._leds_placed: int = 0
        self._state: PatternState = PatternState.fill

    def reset(self):
        self._leds_placed = 0
        self._state = PatternState.fill
    def _apply_to(self, data: list[AddressableLED.LEDData]):
        match self._state:
            case PatternState.fill:
                for i in range(self._bar_size):
                    data[i].setRGB(0, 0, 0)

                for i in range(self._leds_placed + 1):
                    left = i
                    right = self._bar_size - 1 - i
                    if left <= right:
                        data[left].setLED(self._colors[0])
                        data[right].setLED(self._colors[0])

                        self._leds_placed += 1

                        if self._leds_placed > self._center_point:
                            self._state = PatternState.empty

            case PatternState.empty:
                if self._state == PatternState.empty:
                    for i in range(self._bar_size):
                        data[i].setRGB(0, 0, 0)

                    self._leds_placed = 0
                    self._state = PatternState.fill
                    return

    def _correct_gamma(self, color: Color) -> Color:
        return Color(color.red** self._gamma, color.green**self._gamma, color.blue**self._gamma)