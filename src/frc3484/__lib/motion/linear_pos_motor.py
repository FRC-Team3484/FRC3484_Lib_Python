from enum import Enum
from typing import final, override

from math import pi

from wpilib import SmartDashboard
from wpimath.units import feet, feet_per_second, inches

from phoenix6 import controls
from phoenix6.hardware import CANcoder
from phoenix6.configs import CurrentLimitsConfigs, Slot0Configs

from .angular_pos_motor import AngularPositionMotor
from ..datatypes.motion_datatypes import SC_LinearFeedForwardConfig, SC_PIDConfig, SC_MotorConfig, SC_TrapezoidConfig

class State(Enum):
    POWER = 0
    POSITION = 1

@final
class LinearPositionMotor(AngularPositionMotor):
    '''
    Defines a base motor class for angular position control

    Parameters:
        motor_config: SC_TemplateMotorConfig
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
            position_tolerance: feet,
            pulley_radius: inches,
            gear_ratio: float = 1.0,
            external_encoder: CANcoder | None = None
        ) -> None:
        super().__init__(
            motor_config=motor_config, 
            pid_config=pid_config, 
            feed_forward_config=feed_forward_config, 
            trapezoid_config=trapezoid_config, 
            angle_tolerance=position_tolerance, 
            gear_ratio=gear_ratio, 
            external_encoder=external_encoder
        )

        self._open_loop_request: controls.DutyCycleOut = controls.DutyCycleOut(0.0, enable_foc=False)
        self._closed_loop_request: controls.VelocityVoltage = controls.VelocityVoltage(0.0, slot=0, enable_foc=False)

        self._position_tolerance: feet = position_tolerance
        self._pulley_radius: inches = pulley_radius

        self._motor_config.current_limits = CurrentLimitsConfigs() \
            .with_supply_current_limit_enable(motor_config.current_limit_enabled) \
            .with_supply_current_limit(motor_config.current_limit) \
            .with_supply_current_lower_limit(motor_config.current_threshold) \
            .with_supply_current_lower_time(motor_config.current_time) 

        self._motor_config.slot0 = Slot0Configs() \
            .with_k_p(pid_config.Kp) \
            .with_k_i(pid_config.Ki) \
            .with_k_d(pid_config.Kd) \
            .with_k_v(feed_forward_config.V) \
            .with_k_a(feed_forward_config.A) \
            .with_k_s(feed_forward_config.S) \
            .with_k_g(feed_forward_config.G)

        self._motor_motion_magic = self._motor_config.motion_magic
        self._motor_motion_magic.motion_magic_cruise_velocity = trapezoid_config.max_velocity
        self._motor_motion_magic.motion_magic_acceleration = trapezoid_config.max_acceleration
        self._motor_motion_magic.motion_magic_jerk = trapezoid_config.max_jerk

    def at_target_position(self) -> bool:
        '''
        Returns whether the motor is at the target position or not

        Returns:
            - bool: True if the motor is at the target position, False otherwise
        '''
        return abs(self._target_state.position - self.get_position() / self._gear_ratio) < self._position_tolerance

    def get_position(self) -> feet:
        '''
        Returns the current position of the motor

        Returns:
            - feet: The current angle of the motor
        '''
        return super().get_position() * 2 * pi * self._pulley_radius

    @override
    def get_velocity(self) -> feet_per_second:
        '''
        Returns the current velocity of the motor

        Returns:    
            - feet_per_second: The current velocity of the motor
        '''
        return super().get_velocity() * 2 * pi * self._pulley_radius
    
    @override
    def set_target_position(self, position: feet) -> None:
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