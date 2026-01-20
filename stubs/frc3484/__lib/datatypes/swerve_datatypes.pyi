from dataclasses import dataclass
from wpimath.units import amperes as amperes, degrees as degrees, inches as inches, seconds as seconds, volt_seconds_per_meter as volt_seconds_per_meter, volt_seconds_squared_per_meter as volt_seconds_squared_per_meter, volts as volts

volt_seconds_per_rotation = float
volt_seconds_squared_per_rotation = float

@dataclass(frozen=True)
class SC_SwerveConfig:
    drive_can_id: int
    steer_can_id: int
    encoder_can_id: int
    encoder_offset: degrees
    wheel_radius: inches
    drive_gear_ratio: float
    drive_scaling: float = ...
    steer_ratio: float = ...
    steer_motor_reversed: bool = ...
    encoder_reversed: bool = ...

@dataclass(frozen=True)
class SC_SwerveCurrentConfig:
    drive_current_threshold: amperes = ...
    drive_current_time: seconds = ...
    drive_current_limit: amperes = ...
    drive_open_loop_ramp: seconds = ...
    steer_current_threshold: amperes = ...
    steer_current_time: seconds = ...
    steer_current_limit: amperes = ...
    current_limit_enabled: bool = ...

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
