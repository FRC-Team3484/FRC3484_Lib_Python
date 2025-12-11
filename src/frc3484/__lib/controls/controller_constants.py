from enum import Enum, auto
from dataclasses import dataclass

'''
Controller constants for use with the SC_Conroller class.
'''

class _InputType(Enum):
    BUTTON = auto() # True/False

    AXIS = auto() # -1.0 to 1.0
    AXIS_ANGLE = auto() # Degrees: 0-360 or -1 for neutral
    AXIS_MAGNITUDE = auto() # Magnitude of axis movement: 0.0 to 1.0

    TRIGGER = auto() # 0.0 to 1.0

    POV = auto() # Degrees: 0-360 or -1 for neutral
    POV_X = auto() # X component of POV
    POV_Y = auto() # Y component of POV
    POV_ANGLE = auto() # Angle of POV

@dataclass(frozen=True)
class Input:
    '''
    Class for encoding an input type and its indices on the controller.
    For single-index inputs (buttons, axes, triggers), only use the first value.
    '''
    type: _InputType
    index: tuple[int, int]
    
    def __str__(self):
        return f"{self.type.name}({self.index})"
    
@dataclass(frozen=True)
class XboxControllerMap:

    LEFT_JOY_X: Input = Input(_InputType.AXIS, (0, 0)) # -1.0 (left) to 1.0 (right)
    LEFT_JOY_Y: Input = Input(_InputType.AXIS, (1, 0)) # -1.0 (forward) to 1.0 (backward)
    LEFT_JOY_ANGLE: Input = Input(_InputType.AXIS_ANGLE, (0, 1)) # Degrees: 0-360 or -1 for neutral
    LEFT_JOY_MAGNITUDE: Input = Input(_InputType.AXIS_MAGNITUDE, (0, 1)) # Magnitude of left joystick movement: 0.0 to 1.0

    LEFT_TRIGGER: Input = Input(_InputType.TRIGGER, (2, 0)) # 0.0 to 1.0
    RIGHT_TRIGGER: Input = Input(_InputType.TRIGGER, (3, 0)) # 0.0 to 1.0

    RIGHT_JOY_X: Input = Input(_InputType.AXIS, (4, 0)) # -1.0 (left) to 1.0 (right)
    RIGHT_JOY_Y: Input = Input(_InputType.AXIS, (5, 0)) # -1.0 (forward) to 1.0 (backward)
    RIGHT_JOY_ANGLE: Input = Input(_InputType.AXIS_ANGLE, (4, 5)) # Degrees: 0-360 or -1 for neutral
    RIGHT_JOY_MAGNITUDE: Input = Input(_InputType.AXIS_MAGNITUDE, (4, 5)) # Magnitude of right joystick movement: 0.0 to 1.0

    A_BUTTON: Input = Input(_InputType.BUTTON, (1, 0)) # True if pressed
    B_BUTTON: Input = Input(_InputType.BUTTON, (2, 0)) # True if pressed
    X_BUTTON: Input = Input(_InputType.BUTTON, (3, 0)) # True if pressed
    Y_BUTTON: Input = Input(_InputType.BUTTON, (4, 0)) # True if pressed
    LEFT_BUMPER: Input = Input(_InputType.BUTTON, (5, 0)) # True if pressed
    RIGHT_BUMPER: Input = Input(_InputType.BUTTON, (6, 0)) # True if pressed
    BACK_BUTTON: Input = Input(_InputType.BUTTON, (7, 0)) # True if pressed
    START_BUTTON: Input = Input(_InputType.BUTTON, (8, 0)) # True if pressed
    LEFT_STICK_BUTTON: Input = Input(_InputType.BUTTON, (9, 0)) # True if pressed
    RIGHT_STICK_BUTTON: Input = Input(_InputType.BUTTON, (10, 0)) # True if pressed

    DPAD_NONE: Input = Input(_InputType.POV, (0, -1)) # True if neutral
    DPAD_UP: Input = Input(_InputType.POV, (0, 0)) # True if pressed up
    DPAD_RIGHT: Input = Input(_InputType.POV, (0, 90)) # True if pressed right
    DPAD_DOWN: Input = Input(_InputType.POV, (0, 180)) # True if pressed down
    DPAD_LEFT: Input = Input(_InputType.POV, (0, 270)) # True if pressed left
    DPAD_UP_RIGHT: Input = Input(_InputType.POV, (0, 45)) # True if pressed up-right
    DPAD_DOWN_RIGHT: Input = Input(_InputType.POV, (0, 135)) # True if pressed down-right
    DPAD_DOWN_LEFT: Input = Input(_InputType.POV, (0, 225)) # True if pressed down-left
    DPAD_UP_LEFT: Input = Input(_InputType.POV, (0, 315)) # True if pressed up-left

    DPAD_X: Input = Input(_InputType.POV_X, (0, 0)) # -1/0/1 for left/neutral/right
    DPAD_Y: Input = Input(_InputType.POV_Y, (0, 0)) # -1/0/1 for up/neutral/down
    DPAD_ANGLE: Input = Input(_InputType.POV_ANGLE, (0, 0)) # Degrees: 0-360 or -1 for neutral

@dataclass(frozen=True)
class DualShock4Map:

    LEFT_JOY_X: Input = Input(_InputType.AXIS, (0, 0)) # -1.0 (left) to 1.0 (right)
    LEFT_JOY_Y: Input = Input(_InputType.AXIS, (1, 0)) # -1.0 (forward) to 1.0 (backward)
    LEFT_JOY_ANGLE: Input = Input(_InputType.AXIS_ANGLE, (0, 1)) # Degrees: 0-360 or -1 for neutral
    LEFT_JOY_MAGNITUDE: Input = Input(_InputType.AXIS_MAGNITUDE, (0, 1)) # Magnitude of left joystick movement: 0.0 to 1.0

    RIGHT_JOY_X: Input = Input(_InputType.AXIS, (2, 0)) # -1.0 (left) to 1.0 (right)
    RIGHT_JOY_Y: Input = Input(_InputType.AXIS, (5, 0)) # -1.0 (forward) to 1.0 (backward)
    RIGHT_JOY_ANGLE: Input = Input(_InputType.AXIS_ANGLE, (2, 5)) # Degrees: 0-360 or -1 for neutral
    RIGHT_JOY_MAGNITUDE: Input = Input(_InputType.AXIS_MAGNITUDE, (2, 5)) # Magnitude of right joystick movement: 0.0 to 1.0

    L2_TRIGGER: Input = Input(_InputType.TRIGGER, (3, 0)) # 0.0 to 1.0
    R2_TRIGGER: Input = Input(_InputType.TRIGGER, (4, 0)) # 0.0 to 1.0

    SQUARE: Input = Input(_InputType.BUTTON, (1, 0)) # True if pressed
    CROSS: Input = Input(_InputType.BUTTON, (2, 0)) # True if pressed
    CIRCLE: Input = Input(_InputType.BUTTON, (3, 0)) # True if pressed
    TRIANGLE: Input = Input(_InputType.BUTTON, (4, 0)) # True if pressed
    L1: Input = Input(_InputType.BUTTON, (5, 0)) # True if pressed
    R1: Input = Input(_InputType.BUTTON, (6, 0)) # True if pressed
    L2_BUTTON: Input = Input(_InputType.BUTTON, (7, 0)) # True if pressed
    R2_BUTTON: Input = Input(_InputType.BUTTON, (8, 0)) # True if pressed
    SHARE_BUTTON: Input = Input(_InputType.BUTTON, (9, 0)) # True if pressed
    OPTIONS_BUTTON: Input = Input(_InputType.BUTTON, (10, 0)) # True if pressed
    LEFT_STICK_BUTTON: Input = Input(_InputType.BUTTON, (11, 0)) # True if pressed
    RIGHT_STICK_BUTTON: Input = Input(_InputType.BUTTON, (12, 0)) # True if pressed
    PS_BUTTON: Input = Input(_InputType.BUTTON, (13, 0)) # True if pressed
    TOUCHPAD_BUTTON: Input = Input(_InputType.BUTTON, (14, 0)) # True if pressed

    DPAD_NONE: Input = Input(_InputType.POV, (0, -1)) # True if neutral
    DPAD_UP: Input = Input(_InputType.POV, (0, 0))  # True if pressed up
    DPAD_RIGHT: Input = Input(_InputType.POV, (0, 90)) # True if pressed right
    DPAD_DOWN: Input = Input(_InputType.POV, (0, 180)) # True if pressed down
    DPAD_LEFT: Input = Input(_InputType.POV, (0, 270)) # True if pressed left
    DPAD_UP_RIGHT: Input = Input(_InputType.POV, (0, 45)) # True if pressed up-right
    DPAD_DOWN_RIGHT: Input = Input(_InputType.POV, (0, 135)) # True if pressed down-right
    DPAD_DOWN_LEFT: Input = Input(_InputType.POV, (0, 225)) # True if pressed down-left
    DPAD_UP_LEFT: Input = Input(_InputType.POV, (0, 315)) # True if pressed up-left

    DPAD_X: Input = Input(_InputType.POV_X, (0, 0)) # -1/0/1 for left/neutral/right
    DPAD_Y: Input = Input(_InputType.POV_Y, (0, 0)) # -1/0/1 for up/neutral/down
    DPAD_ANGLE: Input = Input(_InputType.POV_ANGLE, (0, 0)) # Degrees: 0-360 or -1 for neutral

@dataclass(frozen=True)
class LogitechExtreme3DMap:

    X: Input = Input(_InputType.AXIS, (0, 0)) # -1.0 (left) to 1.0 (right)
    Y: Input = Input(_InputType.AXIS, (1, 0)) # -1.0 (forward) to 1.0 (backward)
    XY_ANGLE: Input = Input(_InputType.AXIS_ANGLE, (0, 1)) # Degrees: 0-360 or -1 for neutral
    XY_MAGNITUDE: Input = Input(_InputType.AXIS_MAGNITUDE, (0, 1)) # Magnitude of XY movement: 0.0 to 1.0

    Z_ROTATION: Input = Input(_InputType.AXIS, (2, 0)) # -1.0 to 1.0
    THROTTLE: Input = Input(_InputType.AXIS, (3, 0)) # -1.0 to 1.0

    TRIGGER: Input = Input(_InputType.BUTTON, (1, 0)) # True if pressed
    BUTTON_2: Input = Input(_InputType.BUTTON, (2, 0)) # True if pressed
    BUTTON_3: Input = Input(_InputType.BUTTON, (3, 0)) # True if pressed
    BUTTON_4: Input = Input(_InputType.BUTTON, (4, 0)) # True if pressed
    BUTTON_5: Input = Input(_InputType.BUTTON, (5, 0)) # True if pressed
    BUTTON_6: Input = Input(_InputType.BUTTON, (6, 0)) # True if pressed
    BUTTON_7: Input = Input(_InputType.BUTTON, (7, 0)) # True if pressed
    BUTTON_8: Input = Input(_InputType.BUTTON, (8, 0)) # True if pressed
    BUTTON_9: Input = Input(_InputType.BUTTON, (9, 0)) # True if pressed
    BUTTON_10: Input = Input(_InputType.BUTTON, (10, 0)) # True if pressed
    BUTTON_11: Input = Input(_InputType.BUTTON, (11, 0)) # True if pressed
    BUTTON_12: Input = Input(_InputType.BUTTON, (12, 0)) # True if pressed

    HAT_Y: Input = Input(_InputType.AXIS, (4, 0)) # -1/0/1 for up/neutral/down
    HAT_X: Input = Input(_InputType.AXIS, (5, 0)) # -1/0/1 for left/neutral/right