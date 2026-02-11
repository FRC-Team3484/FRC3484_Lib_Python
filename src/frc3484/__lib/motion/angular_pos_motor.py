from enum import Enum
from typing import override

from wpilib import SmartDashboard
from wpimath.units import degrees, degrees_per_second, turns
# from wpimath.controller import PIDController, SimpleMotorFeedforwardMeters
# from wpimath.trajectory import TrapezoidProfile


from phoenix6 import controls
from phoenix6.hardware import CANcoder
from phoenix6.configs import ExternalFeedbackConfigs, FeedbackConfigs, TalonFXSConfiguration, TalonFXConfiguration, CurrentLimitsConfigs, Slot0Configs
from phoenix6.signals import ExternalFeedbackSensorSourceValue, FeedbackSensorSourceValue

from .power_motor import PowerMotor
from ..datatypes.motion_datatypes import SC_AngularFeedForwardConfig, SC_PIDConfig, SC_MotorConfig, SC_TrapezoidConfig

class State(Enum):
    POWER = 0
    POSITION = 1

class AngularPositionMotor(PowerMotor):
    '''
    Defines a base motor class for angular position control

    Parameters:
        motor_config: SC_MotorConfig
        current_config: SC_CurrentConfig
        pid_config: SC_PIDConfig
        feed_forward_config: SC_AngularFeedForwardConfig
        trapezoid_config: SC_TemplateMotorTrapezoidConfig
        angle_tolerance: degrees
        gear_ratio: float = 1.0
        external_encoder: CANcoder | None = None
    '''
    STALL_LIMIT: float = 0.75
    STALL_THRESHOLD: float = 0.1

    def __init__(
            self,
            motor_config: SC_MotorConfig,
            pid_config: SC_PIDConfig,
            feed_forward_config: SC_AngularFeedForwardConfig,
            trapezoid_config: SC_TrapezoidConfig,
            angle_tolerance: degrees,
            gear_ratio: float = 1.0,
            external_encoder: CANcoder | None = None
        ) -> None:
        super().__init__(motor_config)

        # Set up variables
        self._state: State = State.POWER



        self._motor_name: str = str(self._motor.device_id)

        self._encoder: CANcoder | None = external_encoder

        self._gear_ratio: float = gear_ratio
        self._angle_tolerance: degrees = angle_tolerance

        self._open_loop_request: controls.DutyCycleOut = controls.DutyCycleOut(0.0, enable_foc=False)
        self._closed_loop_request: controls.MotionMagicVoltage | controls.PositionVoltage = controls.PositionVoltage(0.0, 0, enable_foc=False) if trapezoid_config == SC_TrapezoidConfig() else controls.MotionMagicVoltage(0.0, slot=0, enable_foc=False)
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

        # Set up motor

        # If the motor_type is minion, it needs a talon FXS controller to be able to set the correct commutation
        # There is no communtation for the falcon, so use a talon FX controller instead
        # The portion for the external encoder is here, but the rest of the configuration is in the PowerMotor class
        if type(self._motor_config) is TalonFXSConfiguration:
            if self._encoder is not None:
                self._gear_ratio = 1.0
                self._motor_config.external_feedback = ExternalFeedbackConfigs() \
                    .with_rotor_to_sensor_ratio(gear_ratio) \
                    .with_feedback_remote_sensor_id(self._encoder.device_id) \
                    .with_external_feedback_sensor_source(ExternalFeedbackSensorSourceValue.REMOTE_CANCODER)

        elif type(self._motor_config) is TalonFXConfiguration:
            if self._encoder is not None:
                self._gear_ratio = 1.0
                self._motor_config.feedback = FeedbackConfigs() \
                    .with_rotor_to_sensor_ratio(gear_ratio) \
                    .with_feedback_remote_sensor_id(self._encoder.device_id) \
                    .with_feedback_sensor_source(FeedbackSensorSourceValue.REMOTE_CANCODER)
        else:
            raise ValueError(f"Invalid motor type: {motor_config.motor_type}")

        _ = self._motor.configurator.apply(self._motor_config)        



    @override
    def periodic(self) -> None:
        '''
        Handles controlling the motors in position mode and printing diagnostics
        '''
        match self._state:
            case State.POSITION:
                self._motor.set_control(self._closed_loop_request)
            case State.POWER:
                self._motor.set_control(self._open_loop_request)
        if SmartDashboard.getBoolean(f"{self._motor_name} Diagnostics", defaultValue=False):
            self.print_diagnostics()

    def at_target_position(self) -> bool:
        '''
        Returns whether the motor is at the target angle or not

        Returns:
            - bool: True if the motor is at the target angle, False otherwise
        '''
        return abs(self._closed_loop_request.position - self._motor.get_position().value) < self._angle_tolerance

    def get_position(self) -> degrees:
        '''
        Returns the current angle of the motor

        Returns:
            - degrees: The current angle of the motor
        '''
        return (self._motor.get_position().value / self._gear_ratio) * 360

    def get_velocity(self) -> degrees_per_second:
        '''
        Returns the current velocity of the motor

        Returns:
            - degrees_per_second: The current velocity of the motor
        '''
        return (self._motor.get_velocity().value / self._gear_ratio) * 360

    def set_power(self, power: float) -> None:
        '''
        Sets the power of the motor

        Parameters:
            - power (float): The power to set the motor to
        '''
        self._open_loop_request.output = power
        self._state = State.POWER

    def set_target_position(self, position: degrees) -> None:
        '''
        Sets the target angle of the motor

        Parameters:
            - angle (degrees): The angle to set the motor to
        '''
        self._closed_loop_request.position = position * (self._gear_ratio * 360)
        self._state = State.POSITION
        


    @override
    def print_diagnostics(self) -> None:
        '''
        Prints diagnostic information to Smart Dashboard
        '''
        _ = SmartDashboard.putNumber(f"{self._motor_name} position (degrees)", self.get_position())
        _ = SmartDashboard.putNumber(f"{self._motor_name} Velocity", self.get_velocity())
        _ = SmartDashboard.putBoolean(f"{self._motor_name} At Target position", self.at_target_position())
        super().print_diagnostics()

    @override
    def set_encoder_position(self, position: turns) -> None:
        '''
        Sets the encoder position of the motor

        Parameters:
            - position (turns): The encoder position to set the motor to
        '''
        return super().set_encoder_position(position * self._gear_ratio)