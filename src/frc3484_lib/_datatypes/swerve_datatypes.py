from dataclasses import dataclass

from wpimath.units import \
    seconds, \
    inches, \
    degrees, \
    volts, \
    amperes, \
    volt_seconds_per_meter, \
    volt_seconds_squared_per_meter


volt_seconds_per_rotation = float
volt_seconds_squared_per_rotation = float

'''
Swerve Drive Datatypes
'''

@dataclass(frozen=True)
class SC_SwerveConfig:
    drive_can_id: int
    steer_can_id: int
    encoder_can_id: int

    encoder_offset: degrees
    wheel_radius: inches
    drive_gear_ratio: float
    drive_scaling: float = 1.0
    steer_ratio: float = 12.8
    
    steer_motor_reversed: bool = True
    encoder_reversed: bool = False

@dataclass(frozen=True)
class SC_SwerveCurrentConfig:
    drive_current_threshold: amperes = 60
    drive_current_time: seconds = 0.1
    drive_current_limit: amperes = 35
    drive_open_loop_ramp: seconds = 0.25

    steer_current_threshold: amperes = 40
    steer_current_time: seconds = 0.1
    steer_current_limit: amperes = 25

    current_limit_enabled: bool = True

@dataclass(frozen=True)
class SC_DrivePIDConfig:
    Kp: float
    Ki: float
    Kd: float
    V: volt_seconds_per_meter
    A: volt_seconds_squared_per_meter
    S: volts

@dataclass(frozen=True)
class SC_SteerPIDConfig:
    Kp: float
    Ki: float
    Kd: float
    V: volt_seconds_per_rotation
    A: volt_seconds_squared_per_rotation
    S: volts