from ..datatypes.motion_datatypes import SC_LinearFeedForwardConfig as SC_LinearFeedForwardConfig, SC_MotorConfig as SC_MotorConfig, SC_PIDConfig as SC_PIDConfig, SC_TrapezoidConfig as SC_TrapezoidConfig
from .angular_pos_motor import AngularPositionMotor as AngularPositionMotor
from enum import Enum
from phoenix6.hardware import CANcoder as CANcoder
from typing import override
from wpimath.units import inches as inches

inches_per_second = float

class State(Enum):
    POWER = 0
    POSITION = 1

class LinearPositionMotor(AngularPositionMotor):
    STALL_LIMIT: float
    STALL_THRESHOLD: float
    def __init__(self, motor_config: SC_MotorConfig, pid_config: SC_PIDConfig, feed_forward_config: SC_LinearFeedForwardConfig, trapezoid_config: SC_TrapezoidConfig, position_tolerance: inches, pulley_radius: inches, gear_ratio: float = 1.0, external_encoder: CANcoder | None = None) -> None: ...
    def at_target_position(self) -> bool: ...
    def get_position(self) -> inches: ...
    @override
    def get_velocity(self) -> inches_per_second: ...
    @override
    def set_target_position(self, position: inches) -> None: ...
    @override
    def print_diagnostics(self) -> None: ...
