from dataclasses import dataclass

from typing import Literal

from phoenix6.signals import NeutralModeValue

from wpimath.units import \
    seconds, \
    volts, \
    amperes, \
    revolutions_per_minute, \
    volt_seconds_per_radian, \
    volt_seconds_squared_per_radian, \
    volt_seconds_per_meter, \
    volt_seconds_squared_per_meter, \
    inches, \
    feet_per_second, \
    feet_per_second_squared, \
    degrees_per_second, \
    degrees_per_second_squared

feet_per_second_cubed = float
degrees_per_second_cubed = float
volt_seconds_per_revolution = float
volt_seconds_squared_per_revolution = float

from wpilib import PneumaticsModuleType

@dataclass(frozen=True)
class SC_LauncherSpeed:
    speed: revolutions_per_minute
    power: float

@dataclass(frozen=True)
class SC_PIDConfig:
    Kp: float = 0.0
    Ki: float = 0.0
    Kd: float = 0.0
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
    G: volts = 0.0
    S: volts = 0.0
    V: volt_seconds_per_radian = 0.0
    A: volt_seconds_squared_per_radian = 0.0

    def __eq__(self, value: object) -> bool:
        if type(value) is SC_AngularFeedForwardConfig:
            if (self.G == value.G) \
            and (self.S == value.S) \
            and (self.V == value.V) \
            and (self.A == value.A):
                return True
            
        return False

@dataclass(frozen=True)
class SC_LinearFeedForwardConfig:
    G: volts = 0.0 
    S: volts = 0.0
    V: volt_seconds_per_meter = 0.0
    A: volt_seconds_squared_per_meter = 0.0

    def __eq__(self, value: object) -> bool:
        if type(value) is SC_LinearFeedForwardConfig:
            if (self.G == value.G) \
            and (self.S == value.S) \
            and (self.V == value.V) \
            and (self.A == value.A):
                return True
            
        return False

@dataclass(frozen=True)
class SC_MotorConfig:
    can_id: int
    inverted: bool = False
    can_bus_name: str = "rio"

    neutral_mode: NeutralModeValue = NeutralModeValue.BRAKE

    motor_type: Literal["falcon", "minion"] = "falcon"

    current_limit_enabled: bool = True
    current_threshold: amperes = 50
    current_time: seconds = 0.1
    current_limit: amperes = 20

@dataclass(frozen=True)
class SC_PositionControl:
    speed: float
    position: inches

@dataclass(frozen=True)
class SC_TrapezoidConfig:
    max_velocity: feet_per_second | degrees_per_second = 0.0
    max_acceleration: feet_per_second_squared | degrees_per_second_squared = 0.0
    max_jerk: feet_per_second_cubed | degrees_per_second_cubed = 0.0

    def __eq__(self, value: object) -> bool:
        if type(value) is SC_TrapezoidConfig:
            if (self.max_velocity == value.max_velocity) \
            and (self.max_jerk == value.max_jerk) \
            and (self.max_acceleration == value.max_acceleration):
                return True
        
        return False


@dataclass(frozen=True)
class SC_ExpoConfig:
    Kv: volt_seconds_per_revolution
    Ka: volt_seconds_squared_per_revolution
