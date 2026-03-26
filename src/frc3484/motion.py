from .__lib.motion.angular_pos_motor import AngularPositionMotor
from .__lib.motion.linear_pos_motor import LinearPositionMotor
from .__lib.motion.power_motor import PowerMotor
from .__lib.motion.velocity_motor import VelocityMotor
from .__lib.motion.expo_motor import ExpoMotor

from .__lib.datatypes.motion_datatypes import \
    SC_SpeedRequest, \
    SC_PIDConfig, \
    SC_SolenoidConfig, \
    SC_DoubleSolenoidConfig, \
    SC_AngularFeedForwardConfig, \
    SC_LinearFeedForwardConfig, \
    SC_MotorConfig, \
    SC_PositionControl, \
    SC_LinearTrapezoidConfig, \
    SC_AngularTrapezoidConfig, \
    SC_ExpoConfig

__all__ = [
    "AngularPositionMotor",
    "LinearPositionMotor",
    "PowerMotor",
    "VelocityMotor",
    "ExpoMotor",
    "SC_SpeedRequest",
    "SC_PIDConfig",
    "SC_SolenoidConfig",
    "SC_DoubleSolenoidConfig",
    "SC_AngularFeedForwardConfig",
    "SC_LinearFeedForwardConfig",
    "SC_MotorConfig",
    "SC_PositionControl",
    "SC_LinearTrapezoidConfig",
    "SC_AngularTrapezoidConfig",
    "SC_ExpoConfig"
]