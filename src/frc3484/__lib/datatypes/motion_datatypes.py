from dataclasses import dataclass

from wpimath.units import \
    seconds, \
    volts, \
    amperes, \
    revolutions_per_minute, \
    volt_seconds_per_radian, \
    volt_seconds_squared_per_radian, \
    volt_seconds_per_meter, \
    volt_seconds_squared_per_meter

from wpilib import PneumaticsModuleType

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