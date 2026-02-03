from wpilib import AddressableLED, Color
from wpimath.units import meters_per_second
from typing import Iterable

from enum import Enum

class PatternState(Enum):
    fill = 0,
    empty = 1

class ColorStack :
    def __init__(self, colors: Iterable[Color], bar_size: int, velocity: meters_per_second, fill_size: int, empty_size: int, gamma: float) -> None:
        self._colors: list[Color] = []
        for color in colors:
            self._colors.append(self._correct_gamma(color))
        self._bar_size = bar_size
        self._velocity = velocity
        self._fill_size = fill_size
        self._empty_size = empty_size
        self._gamma = gamma
        self._state: PatternState = PatternState.fill
        self._leds_placed: int = 0
        self._falling_led_position: float = 0.0
        self.reset()
    def reset(self):
        self._leds_placed = 0
        self._falling_led_position = 0
        self._state = PatternState.fill
    def _apply_to(self, data: list[AddressableLED.LEDData]):
        match self._state:
            case PatternState.fill:
                for i in range(len(data)):
                    if(i >= (len(data)) - self._leds_placed):
                        data[i].setLED(self._correct_gamma(self._colors[self._get_color_index(i)]))
                    elif(i >= int(self._falling_led_position) and i < int(self._falling_led_position) + self._fill_size):
                        data[i].setLED(self._correct_gamma(self._colors[self._get_color_index(len(data)) - self._leds_placed - self._fill_size + i - int(self._falling_led_position)]))
                    else:
                        data[i].setLED(Color.kBlack)
                self._falling_led_position += self._velocity
                if(int(self._falling_led_position) >= (len(data)) - self._leds_placed - self._fill_size):
                    self._falling_led_position = 0
                    self._leds_placed += self._fill_size
                    if(self._leds_placed >= (len(data))):
                        self._falling_led_position = (len(data))
                        self._leds_placed = (len(data))
                        self._state = PatternState.empty
                return data
            case PatternState.empty:
                for i in range(len(data)):
                    if(i < self._leds_placed):
                        data[i].setLED(self._correct_gamma(self._colors[self._get_color_index(i)]))
                    elif(i >= int(self._falling_led_position) and i < int(self._falling_led_position) + self._empty_size):
                        data[i].setLED(self._correct_gamma(self._colors[self._get_color_index(self._leds_placed + i - int(self._falling_led_position))]))
                    else:
                        data[i].setLED(Color.kBlack)
                self._falling_led_position += self._velocity
                if(int(self._falling_led_position) >= (len(data))):
                    self._leds_placed -= self._fill_size
                    self._falling_led_position = self._leds_placed
                    if(self._leds_placed > (len(data))):
                        self.reset()
                return data

    def _get_color_index(self, offset: int) -> int:
        return (offset // self._bar_size) % len(self._colors)
    def  _positive_fmod(self, numerator: float, denominator: float)-> float:
        return ((numerator % denominator) + denominator % denominator)
    def _correct_gamma(self, color: Color) -> Color:
        return Color(color.red** self._gamma, color.green**self._gamma, color.blue**self._gamma)