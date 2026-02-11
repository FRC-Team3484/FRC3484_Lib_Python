from enum import Enum
from typing import final, override

from math import pi

from wpilib import SmartDashboard
from wpimath.units import inches, radiansToDegrees, inchesToMeters
inches_per_second = float

from phoenix6.hardware import CANcoder
# from phoenix6 import controls
# from phoenix6.configs import CurrentLimitsConfigs, Slot0Configs

from .angular_pos_motor import AngularPositionMotor
from ..datatypes.motion_datatypes import SC_LinearFeedForwardConfig, SC_AngularFeedForwardConfig, SC_PIDConfig, SC_MotorConfig, SC_TrapezoidConfig

class State(Enum):
    POWER = 0
    POSITION = 1

@final
class LinearPositionMotor(AngularPositionMotor):
    '''
    Defines a base motor class for angular position control

    Parameters:
        motor_config: SC_MotorConfig
        current_config: SC_TemplateMotorCurrentConfig
        pid_config: SC_PIDConfig
        feed_forward_config: SC_LinearFeedForwardConfig
        trapezoid_config: SC_TemplateMotorTrapezoidConfig
        position_tolerance: feet
        gear_ratio: float = 1.0
        external_encoder: CANcoder | None = None
    '''
    STALL_LIMIT: float = 0.75
    STALL_THRESHOLD: float = 0.1

    def __init__(
            self,
            motor_config: SC_MotorConfig,
            pid_config: SC_PIDConfig,
            feed_forward_config: SC_LinearFeedForwardConfig,
            trapezoid_config: SC_TrapezoidConfig,
            position_tolerance: inches,
            pulley_radius: inches,
            gear_ratio: float = 1.0,
            external_encoder: CANcoder | None = None
        ) -> None:
        
        angular_feed_forward_config = SC_AngularFeedForwardConfig(
            feed_forward_config.G,
            feed_forward_config.S,
            feed_forward_config.V * inchesToMeters(pulley_radius),
            feed_forward_config.A * inchesToMeters(pulley_radius)
        )

        super().__init__(
            motor_config=motor_config, 
            pid_config=pid_config, 
            feed_forward_config=angular_feed_forward_config, 
            trapezoid_config=trapezoid_config, 
            angle_tolerance=radiansToDegrees(position_tolerance/pulley_radius), 
            gear_ratio=gear_ratio, 
            external_encoder=external_encoder
        )

        
        self._pulley_radius: inches = pulley_radius
        

    def at_target_position(self) -> bool:
        '''
        Returns whether the motor is at the target position or not

        Returns:
            - bool: True if the motor is at the target position, False otherwise
        '''
        return super().at_target_position() # abs(self._target_state.position - self.get_position() / self._gear_ratio) < self._position_tolerance

    def get_position(self) -> inches:
        '''
        Returns the current position of the motor

        Returns:
            - feet: The current angle of the motor
        '''
        return (super().get_position()/360) * 2 * pi * self._pulley_radius

    @override
    def get_velocity(self) -> inches_per_second:
        '''
        Returns the current velocity of the motor

        Returns:    
            - feet_per_second: The current velocity of the motor
        '''
        return (super().get_velocity()/360) * 2 * pi * self._pulley_radius
    
    @override
    def set_target_position(self, position: inches) -> None:
        '''
        Sets the target position of the motor

        Parameters:
            - position (feet): The angle to set the motor to
        '''
        super().set_target_position(position * self._gear_ratio)

    @override
    def print_diagnostics(self) -> None:
        '''
        Prints diagnostic information to Smart Dashboard
        '''
        _ = SmartDashboard.putNumber(f"{self._motor_name} Position (feet)", self.get_position())
        _ = SmartDashboard.putNumber(f"{self._motor_name} Velocity (feet/s)", self.get_velocity())
        _ = SmartDashboard.putBoolean(f"{self._motor_name} At Target Position", self.at_target_position())
        return super().print_diagnostics()

    @override
    def set_encoder_position(self, position: inches) -> None:
        '''
        Sets the encoder position of the motor

        Parameters:
            - position (inches): The encoder position to set the motor to
        '''
        return super().set_encoder_position((position / self._pulley_radius) / (2 * pi))