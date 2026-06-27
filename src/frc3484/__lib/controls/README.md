# Controls
This document describes how to use the various controller features in the lib.

This is generally just a more robust way of creating controller buttons for OI, with an abstraction layer. This lets you easily define triggers or POVs (which are usually in a range of 0 to 1) as a button, returning either a true or false.

## Creating Constant Input Bindings
Usually, you would want to first define a more human readable name for each button. These are placed in `constants.py`, and allow you to change button bindings later by editing the constants, instead of having to directly change code in OI.

```py
# constants.py
from frc3484.controls import XboxControllerMap as ControllerMap

# Some bindings you would usually want for a driver are omitted here
class UserInterface:
    class Driver:
        CONTROLLER_PORT: int = 0
        JOYSTICK_DEADBAND: float = 0.02
        AXIS_LIMIT: float = 0.5
        TRIGGER_LIMIT: float = 0.5

        THROTTLE_AXIS: Input = ControllerMap.LEFT_JOY_Y
        STRAFE_AXIS: Input = ControllerMap.LEFT_JOY_X
        ROTATION_AXIS: Input = ControllerMap.RIGHT_JOY_X

        JOG_UP_BUTTON: Input = ControllerMap.DPAD_UP
        JOG_DOWN_BUTTON: Input = ControllerMap.DPAD_DOWN
        JOG_LEFT_BUTTON: Input = ControllerMap.DPAD_LEFT
        JOG_RIGHT_BUTTON: Input = ControllerMap.DPAD_RIGHT
```

## Creating Functions for Each Input
Then, you will create a class in `oi.py` for these bindings. Create a `SC_Controller` object for each controller you want to listen to, using the options from your constant class for that controller.

With this `SC_Controller` object, you will then create functions that check each of the constant bindings, and return the information you want to use in code.

```py
# oi.py
from frc3484.controls import SC_Controller

from src.constants import UserInterface

# Some bindings you would usually want for a driver are omitted here
class DriverInterface:
    _controller: SC_Controller = SC_Controller(
        UserInterface.Driver.CONTROLLER_PORT,
        UserInterface.Driver.AXIS_LIMIT,
        UserInterface.Driver.TRIGGER_LIMIT,
        UserInterface.Driver.JOYSTICK_DEADBAND
    )

    def __init__(self) -> None:
        pass

    def get_throttle(self) -> float:
        return self._controller.get_axis(UserInterface.Driver.THROTTLE_AXIS)
    def get_strafe(self) -> float:
        return self._controller.get_axis(UserInterface.Driver.STRAFE_AXIS)
    def get_rotation(self) -> float:
        return -self._controller.get_axis(UserInterface.Driver.ROTATION_AXIS)
    
    def get_jog_up(self) -> bool:
        return self._controller.get_button(UserInterface.Driver.JOG_UP_BUTTON)
    def get_jog_down(self) -> bool:
        return self._controller.get_button(UserInterface.Driver.JOG_DOWN_BUTTON)
    def get_jog_left(self) -> bool:
        return self._controller.get_button(UserInterface.Driver.JOG_LEFT_BUTTON)
    def get_jog_right(self) -> bool:
        return self._controller.get_button(UserInterface.Driver.JOG_RIGHT_BUTTON)
```

Notice that some custom manipulation can be done in `oi.py`. Above, the value returned from `get_rotation` is inverted, because that feels more intuitive when driving.

You could also limit speeds of some values:
```py
# oi.py
class DemoInterface:
    _controller: SC_Controller = SC_Controller(
        UserInterface.Demo.CONTROLLER_PORT,
        UserInterface.Demo.AXIS_LIMIT,
        UserInterface.Demo.TRIGGER_LIMIT,
        UserInterface.Demo.JOYSTICK_DEADBAND
    )

    def get_throttle(self) -> float:
        return self._controller.get_axis(UserInterface.Demo.THROTTLE_AXIS) * 0.1 # Limited to 10% power
```

Notice that you can also use an input from constants that is usually used as an axis (or 0 to 1 value) as a true or false instead:
```py
# oi.py
class DriverInterface:
    _controller: SC_Controller = SC_Controller(
        UserInterface.Driver.CONTROLLER_PORT,
        UserInterface.Driver.AXIS_LIMIT,
        UserInterface.Driver.TRIGGER_LIMIT,
        UserInterface.Driver.JOYSTICK_DEADBAND
    )

    def get_throttle(self) -> float:
        return self._controller.get_button(ControllerMap.LEFT_JOY_Y) # Instead of returning a float, this just returns a true or false
```

Without this, you would have to have extra code in `oi.py` for converting that range to a true or false instead.

## Using Input Functions Elsewhere
With these functions created in `oi.py`, they can be used in commands to react to user input.

```py
class IndexerTestCommand(Command):
    def __init__(self, oi: TestInterface1, indexer_subsystem: IndexerSubsystem) -> None:
        super().__init__()
        self._oi: TestInterface1 = oi
        self._indexer_subsystem: IndexerSubsystem = indexer_subsystem

    @override
    def execute(self) -> None:
        self._indexer_subsystem.set_power(
            self._oi.get_indexer() # Set the indexer power to the value of the function from OI
        )
    
    @override
    def end(self, interrupted: bool) -> None:
        self._indexer_subsystem.set_power(0)
    
    @override
    def isFinished(self) -> bool:
        return False
```