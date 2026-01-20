from dataclasses import dataclass
from phoenix6.signals import NeutralModeValue
from typing import Literal
from wpilib import PneumaticsModuleType as PneumaticsModuleType
from wpimath.units import amperes as amperes, degrees_per_second as degrees_per_second, degrees_per_second_squared as degrees_per_second_squared, feet_per_second as feet_per_second, feet_per_second_squared as feet_per_second_squared, inches as inches, revolutions_per_minute as revolutions_per_minute, seconds as seconds, volt_seconds_per_meter as volt_seconds_per_meter, volt_seconds_per_radian as volt_seconds_per_radian, volt_seconds_squared_per_meter as volt_seconds_squared_per_meter, volt_seconds_squared_per_radian as volt_seconds_squared_per_radian, volts as volts

feet_per_second_cubed = float
degrees_per_second_cubed = float

@dataclass(frozen=True)
class SC_LauncherSpeed:
    speed: revolutions_per_minute
    power: float

@dataclass(frozen=True)
class SC_PIDConfig:
    Kp: float
    Ki: float
    Kd: float
    Kf: float = ...

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
    inverted: bool = ...
    can_bus_name: str = ...
    neutral_mode: NeutralModeValue = ...
    motor_type: Literal['falcon', 'minion'] = ...
    current_limit_enabled: bool = ...
    current_threshold: amperes = ...
    current_time: seconds = ...
    current_limit: amperes = ...

@dataclass(frozen=True)
class SC_PositionControl:
    speed: float
    position: inches

@dataclass(frozen=True)
class SC_TrapezoidConfig:
    max_velocity: feet_per_second | degrees_per_second
    max_acceleration: feet_per_second_squared | degrees_per_second_squared
    max_jerk: feet_per_second_cubed | degrees_per_second_cubed
