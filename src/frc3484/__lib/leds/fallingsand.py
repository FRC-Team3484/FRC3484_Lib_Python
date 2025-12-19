from wpilib import AddressableLED, Color
from wpimath.units import meters, meters_per_second, meters_per_second_squared
from typing import Iterable

from enum import Enum

class PatternState(Enum):
    fill = 0,
    empty = 1

class FallingSand:
    def __init__(self, colors: Iterable[Color], bar_size: int, led_spacing: meters, intake_velocity: meters_per_second, exit_acceleration: meters_per_second_squared, fill_size: int, gamma: float) -> None:
        self._colors: list[Color] = []
        for color in colors:
            self._colors.append(self._correct_gamma(color))
        self._bar_size: int = bar_size
        self._led_spacing: meters = led_spacing
        self._intake_velocity: meters_per_second = intake_velocity
        self._exit_acceleration: meters_per_second_squared = exit_acceleration
        self._exit_velocity = intake_velocity + exit_acceleration * 0.5
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

    def _apply_to(self, data: list[AddressableLED.LEDData]):
        match self._state: 
            case PatternState.fill:
                for i in range(len(data)):
                    if (i >= (len(data)) - self._leds_placed) :
                        data[i].setLED(self._correct_gamma(self._colors[self._get_color_index(i)]))
                    elif(i >= int(self._falling_led_position) and i < int(self._falling_led_position) + self._fill_size) :
                        data[i].setLED(self._correct_gamma(self._colors[self._get_color_index(len(data) - self._leds_placed - self._fill_size + i)]))
                    else:
                        data[i].setLED(Color.kBlack)
                self._falling_led_position += self._intake_velocity
                if (int(self._falling_led_position) >= (len(data) - self._leds_placed - self._fill_size)) :
                    self._falling_led_position = 0
                    self._leds_placed += self._fill_size
                    if (self._leds_placed > (len(data))) :
                        self._falling_led_position = (len(data))
                        self._leds_placed = (len(data))
                        self._state = PatternState.empty
            case PatternState.empty:
                self._falling_led_position += self._exit_velocity
                self._exit_velocity += self._exit_acceleration
                for i in range(len(data)):
                    if (i<int(self._falling_led_position)):
                        data[i].setLED(Color.kBlack)
                    else:
                        data[i].setLED(self._colors[self._get_color_index(i - int(self._falling_led_position))])
                if(self._falling_led_position >= (len(data))):
                    self.reset()

    def _get_color_index(self, offset: int) -> int:
        return (offset // self._bar_size) % len(self._colors) 
    def  _positive_fmod(self, numerator: float, denominator: float)-> float:
        return ((numerator % denominator) + denominator % denominator)
    def _correct_gamma(self, color: Color) -> Color:
        return Color(color.red** self._gamma, color.green**self._gamma, color.blue**self._gamma)