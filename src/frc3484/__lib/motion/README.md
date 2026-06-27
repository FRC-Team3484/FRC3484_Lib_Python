# Motion
This document describes how to use the various motion features in this lib.

Motion classes here represent a common type of CTRE motor. Depending on the type of motor, they include Motion Magic (PID and Feed Forward), current limits, remote Cancoders, SmartDashboard diagnostics, data logging, motor following, SysID logging, and more. All of this is usable with nice typed configuration parameters, making it extremely easy to create subsystems.

## Power Motor
A power motor is a motor that is simply controlled using a power from -100% to +100%. Useful for simple spinning mechanisms, that do not need to account or compensate for outside forces.

First, create its configuration:
```py
# constants.py
from frc3484.motion import SC_MotorConfig

class PowerMotorConstants:
    POWER_MOTOR_CONFIG: SC_MotorConfig = SC_MotorConfig(
        can_id=0,
        inverted=False,
        neutral_mode=NeutralModeValue.COAST,
        motor_name="power_motor"
    )
```

Then, create the motor object in your subsystem:
```py
# subsystem.py
from frc3484.motion import PowerMotor

from constants import PowerMotorConstants

_power_motor: PowerMotor = PowerMotor(
    motor_config=PowerMotorConstants.ROLLER_MOTOR_CONFIG, 
    logging_enabled=True
)
```

Now you can control and get values from that motor:
```py
# subsystem.py

_power_motor.set_power(0.5) # Set the motor to 50% power
_power_motor.set_power(-0.2) # Set the motor to go backwards at 20% power

_power_motor.set_brake_mode() # Put the motor into brake mode
_power_motor.print_diagnostics() # Print motor diagnostics to SmartDashboard 
```

## Velocity Motor
A motor that accelerates to or from a given speed and holds at that speed. Useful for spinning mechanisms that need to smoothly accelerate to and stay at a specific speed.

This motor will need to be tuned to obtain PID and feed forward values. This can be done by hand using Phoenix Tuner, or by running SysID routines.

When setting the speed for this motor, it takes a `SC_SpeedRequest`. This takes both a `speed` (`revolutions_per_minute`) and `power` (`int`), If `speed` is provided, the motor will run in a closed loop (with the PID and feed forward correction). If just a `power` is provided, the motor will run in regular power mode. With both, `power` is ignored.

First, create this motor's configuration:
```py
# constants.py
from frc3484.motion import SC_MotorConfig, SC_PIDConfig, SC_AngularFeedForwardConfig

class VelocityMotorConstants:
    VELOCITY_MOTOR_CONFIG: SC_MotorConfig = SC_MotorConfig(
        can_id=0,
        inverted=False,
        can_bus_name="rio",
        neutral_mode=NeutralModeValue.COAST,
        motor_type = "falcon",
        current_limit_enabled=True,
        current_threshold=0,
        current_time=0.0,
        current_limit=30,
        motor_name="velocity_motor"
    )
    PID_CONFIG: SC_PIDConfig = SC_PIDConfig(
        Kp=0.0,
        Ki=0.0,
        Kd=0.0,
        Kf=0.0
    )
    FEED_FORWARD_CONFIG: SC_AngularFeedForwardConfig = SC_AngularFeedForwardConfig(
        G=0.0,
        S=0.0,
        V=0.0,
        A=0.0
    )
    TOLERANCE: float = 50 / 60 # rpm
    GEAR_RATIO: float = 1.0
```

Then, create the motor object in your subsystem:
```py
# subsystem.py
from frc3484.motion import VelocityMotor

from constants import VelocityMotorConstants

_velocity_motor: VelocityMotor = VelocityMotor(
    motor_config=VelocityMotorConstants.MOTOR_CONFIG,
    pid_config=VelocityMotorConstants.PID_CONFIG,
    feed_forward_config=VelocityMotorConstants.FEED_FORWARD_CONFIG,
    gear_ratio=VelocityMotorConstants.GEAR_RATIO,
    tolerance=VelocityMotorConstants.TOLERANCE,
    logging_enabled=True
)
```

Now you can control and get values from that motor:
```py
# subsystem.py
from wpimath.units import revolutions_per_minute

from frc3484.motion import SC_SpeedRequest

_velocity_motor.set_mechanism_speed(SC_SpeedRequest(speed=800, power=0)) # Run the motor at 800 RPMs
_velocity_motor.set_mechanism_speed(SC_SpeedRequest(speed=0, power=0.5)) # Run the motor at 50% power

current_speed: revolutions_per_minute = _velocity_motor.get_mechanism_speed()

_velocity_motor.set_brake_mode() # Put the motor into brake mode
_velocity_motor.print_diagnostics() # Print motor diagnostics to SmartDashboard 
```

## Angular Position Motor
A motor that accelerates to or from a given angular position, and holds at that location. Useful for a mechanism that moves in an arc or circle, where it needs to hold a position along that circle.

This motor will need to be tuned to obtain PID and feed forward values. This can be done by hand using Phoenix Tuner, or by running SysID routines.

First, create this motor's configuration:
```py
# constants.py
from wpimath.units import degrees

from frc3484.motion import SC_MotorConfig, SC_PIDConfig, SC_AngularFeedForwardConfig, SC_AngularTrapezoidConfig

class AngularPositionMotorConstants:
    ANGULAR_POSITION_MOTOR_CONFIG: SC_MotorConfig = SC_MotorConfig(
        can_id=0,
        motor_type="minion",
        inverted=False,
        motor_name="angular_position_motor"
    )
    PID_CONFIG: SC_PIDConfig = SC_PIDConfig(
        Kp=0.0,
        Ki=0.0,
        Kd=0.0,
        Kf=0.0
    )
    FEED_FORWARD_CONFIG: SC_AngularFeedForwardConfig = SC_AngularFeedForwardConfig(
        G=0.0,
        S=0.0,
        V=0.0,
        A=0.0
    )
    TRAPEZOID_CONFIG: SC_AngularTrapezoidConfig = SC_AngularTrapezoidConfig(
        max_velocity=0.0, # rev/s
        max_acceleration=480.0 # rev/s^2
    )
    ANGLE_TOLERANCE: degrees = 5.0
    GEAR_RATIO: float = 23.0
```

Next, create the motor object in your subsystem:
```py
# subsystem.py
from frc3484.motion import AngularPositionMotor

from constants import AngularPositionMotorConstants

_angular_position_motor: AngularPositionMotor = AngularPositionMotor(
    motor_config=AngularPositionMotorConstants.ANGULAR_POSITION_MOTOR_CONFIG, 
    pid_config=AngularPositionMotorConstants.PID_CONFIG, 
    feed_forward_config=AngularPositionMotorConstants.FEED_FORWARD_CONFIG, 
    trapezoid_config=AngularPositionMotorConstants.TRAPEZOID_CONFIG, 
    angle_tolerance=AngularPositionMotorConstants.ANGLE_TOLERANCE, 
    gear_ratio=AngularPositionMotorConstants.GEAR_RATIO,
    logging_enabled=True
)
```

Now you can control and get values from that motor:
```py
# subsystem.py
from wpimath.units import degrees_per_second

_angular_position_motor.set_target_position(45) # Set the motor to 45 degrees
at_target_position: bool = _angular_position_motor.at_target_position()
current_velocity: degrees_per_second = _angular_position_motor.get_velocity()

_angular_position_motor.set_brake_mode() # Put the motor into brake mode
_angular_position_motor.print_diagnostics() # Print motor diagnostics to SmartDashboard 
```

## Expo Motor
An angular position motor, but using an exponential acceleration curve instead of a trapezoidal one.

Creating an expo motor is the same as creating an angular position motor, except you use the `ExpoMotor` class instead:
```py
# subsystem.py
from frc3484.motion import ExpoMotor

from constants import ExpoMotorConstants

_expo_motor: ExpoMotor = ExpoMotor(
    motor_config=ExpoMotorConstants.EXPO_MOTOR_CONFIG, 
    pid_config=ExpoMotorConstants.PID_CONFIG, 
    feed_forward_config=ExpoMotorConstants.FEED_FORWARD_CONFIG, 
    trapezoid_config=ExpoMotorConstants.TRAPEZOID_CONFIG, 
    angle_tolerance=ExpoMotorConstants.ANGLE_TOLERANCE, 
    gear_ratio=ExpoMotorConstants.GEAR_RATIO,
    logging_enabled=True
)
```

## Linear Position Motor
A motor that accelerates to or from a given linear position, and holds at that location. Useful for a mechanism that moves in a straight line, where it needs to hold a position somewhere along that line.

This motor will need to be tuned to obtain PID and feed forward values. This can be done by hand using Phoenix Tuner, or by running SysID routines.

Creating a linear position motor is similar to the angular position one, except a different datatype is used for the `feed_forward_config` and `trapezoid_config`:
```py
# constants.py
from wpimath.units import degrees

from frc3484.motion import SC_MotorConfig, SC_PIDConfig, SC_LinearFeedForwardConfig, SC_AngularTrapezoidConfig

class AngularPositionMotorConstants:
    ...
    FEED_FORWARD_CONFIG: SC_LinearFeedForwardConfig = SC_LinearFeedForwardConfig(
        G=0.0,
        S=0.0,
        V=0.0,
        A=0.0
    )
    TRAPEZOID_CONFIG: SC_LinearTrapezoidConfig = SC_LinearTrapezoidConfig(
        max_velocity=0.0, # feet/s
        max_acceleration=480.0 # feet/s^2
    )
    ...
```

Then, create your motor class:
```py
# subsystem.py
from frc3484.motion import LinearPositionMotor

from constants import LinearPositionMotorConstants

_linear_position_motor: LinearPositionMotor = LinearPositionMotor(
    motor_config=LinearPositionMotorConstants.LINEAR_POSITION_MOTOR_CONFIG, 
    pid_config=LinearPositionMotorConstants.PID_CONFIG, 
    feed_forward_config=LinearPositionMotorConstants.FEED_FORWARD_CONFIG, 
    trapezoid_config=LinearPositionMotorConstants.TRAPEZOID_CONFIG, 
    angle_tolerance=LinearPositionMotorConstants.ANGLE_TOLERANCE, 
    gear_ratio=LinearPositionMotorConstants.GEAR_RATIO,
    logging_enabled=True
)
```

Now you can control and get values from that motor:
```py
# subsystem.py
from wpimath.units import feet_per_second

_linear_position_motor.set_target_position(24) # Set the motor to 24 inches
at_target_position: bool = _linear_position_motor.at_target_position()
current_velocity: feet_per_second = _linear_position_motor.get_velocity()

_linear_position_motor.set_brake_mode() # Put the motor into brake mode
_linear_position_motor.print_diagnostics() # Print motor diagnostics to SmartDashboard 
```