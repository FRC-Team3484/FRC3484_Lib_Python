from wpilib import AddressableLED, LEDPattern, Timer, Color
from enum import Enum

class PatternState(Enum):
    fill = 0,
    empty = 1

class Static:
    def __init__(self) -> None:
        pass