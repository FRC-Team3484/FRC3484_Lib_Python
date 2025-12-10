from wpimath.units import \
    seconds, \
    inches, \
    degrees, \
    volts, \
    amperes, \
    revolutions_per_minute, \
    radians_per_second, \
    radians_per_second_squared, \
    volt_seconds_per_meter, \
    volt_seconds_squared_per_meter, \
    volt_seconds_per_radian, \
    volt_seconds_squared_per_radian

from wpilib import PneumaticsModuleType
from wpimath.geometry import Transform3d, Pose2d

from dataclasses import dataclass

'''
Motion Control Datatypes
'''

@dataclass(frozen=True)
class SC_LauncherSpeed:
    speed: revolutions_per_minute
    power: float

@dataclass(frozen=True)
class SC_PIDConfig:
    Kp: float
    Ki: float
    Kd: float
    Kf: float = 0.0

@dataclass(frozen=True)
class SC_SolenoidConfig:
    controller_id: int
    channel: int
    module_type: PneumaticsModuleType
@dataclass(frozen=True)
class SC_DoubleSolenoidConfig:
    controller_id: int
    forward_channel: int
    reverse_channel: int
    module_type: PneumaticsModuleType

@dataclass(frozen=True)
class SC_AngularFeedForwardConfig:
    G: volts
    S: volts
    V: volt_seconds_per_radian
    A: volt_seconds_squared_per_radian

@dataclass(frozen=True)
class SC_LinearFeedForwardConfig:
    G: volts
    S: volts
    V: volt_seconds_per_meter
    A: volt_seconds_squared_per_meter

@dataclass(frozen=True)
class SC_MotorConfig:
    can_id: int
    inverted: bool = False
    can_bus_name: str = "rio"
    
    current_limit_enabled: bool = True
    current_threshold: amperes = 50
    current_time: seconds = 0.1
    current_limit: amperes = 20

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
    max_speed: radians_per_second
    max_acceleration: radians_per_second_squared

'''
Vision Datatypes
'''

@dataclass(frozen=True)
class SC_CameraConfig:
    name: str
    position: Transform3d
    enabled: bool = True

@dataclass(frozen=True)
class SC_CameraResults:
    vision_measurement: Pose2d
    timestamp: seconds
    standard_deviation: tuple[float, float, float]