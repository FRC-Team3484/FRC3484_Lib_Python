from typing import override
from math import tau

from wpilib import DataLogManager, SmartDashboard
from wpimath.units import revolutions_per_minute, radians_per_second
from wpiutil.log import BooleanLogEntry, DoubleLogEntry

from phoenix6 import controls
from phoenix6.configs import CurrentLimitsConfigs, Slot0Configs, TalonFXConfiguration, TalonFXSConfiguration

from ..datatypes.motion_datatypes import SC_AngularFeedForwardConfig, SC_PIDConfig, SC_MotorConfig, SC_SpeedRequest

from .power_motor import PowerMotor

class VelocityMotor(PowerMotor):
    '''
    Creates a motor template class that represents a motor that can be set to a target speed

    Parameters:
        - motor_config (SC_MotorConfig): The configuration for the motor
        - current_config (SC_TemplateMotorCurrentConfig): Current limit settings for the motor
        - pid_config (SC_PIDConfig): The configuration for the PID controller
        - gear_ratio (float): The gear ratio of the motor
        - tolerance (revolutions_per_minute): The tolerance for the target speed to consider it reached
        - logging_enabled (bool): Whether logging is enabled for this motor
    '''

    def __init__(
        self, 
        motor_config: SC_MotorConfig, 
        pid_config: SC_PIDConfig, 
        feed_forward_config: SC_AngularFeedForwardConfig,
        gear_ratio: float, 
        tolerance: revolutions_per_minute,
        logging_enabled: bool
    ) -> None:
        
        super().__init__(motor_config, logging_enabled)

        self._tolerance: revolutions_per_minute = tolerance

        self._open_loop_request: controls.DutyCycleOut = controls.DutyCycleOut(0.0, enable_foc=False)
        self._closed_loop_request: controls.VelocityVoltage = controls.VelocityVoltage(0.0, slot=0, enable_foc=False)

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
        
        if type(self._motor_config) is TalonFXConfiguration:
            self._motor_config.feedback.sensor_to_mechanism_ratio = gear_ratio
        elif type(self._motor_config) is TalonFXSConfiguration:
            self._motor_config.external_feedback.sensor_to_mechanism_ratio = gear_ratio

        
        self._motor.configurator.apply(self._motor_config)  # type: ignore

        self._logging_enabled = logging_enabled
        if self._logging_enabled:
            self._speed_log = DoubleLogEntry(DataLogManager.getLog(), f"/motors/{self._name}/speed_rpm")
            self._at_target_speed_log = BooleanLogEntry(DataLogManager.getLog(), f"/motors/{self._name}/at_target_speed")

    @override
    def periodic(self) -> None:
        '''
        Handles Smart Dashboard diagnostic information and actually controlling the motors
        '''

        if self._closed_loop_request.velocity != 0.0:
            self._motor.set_control(self._closed_loop_request)
        else:
            self._motor.set_control(self._open_loop_request)
    
    def set_mechanism_speed(self, speed: SC_SpeedRequest) -> None:
        '''
        Sets the target speed for the motor

        Parameters:
            - speed (SC_TemplateMotorVelocityControl): The speed and power to set the motor to
        '''
        self._open_loop_request.output = speed.power
        self._closed_loop_request.velocity = (speed.speed) / 60

    def get_mechanism_speed(self) -> revolutions_per_minute:
        '''
        Returns the current speed of the mechanism in RPM

        Returns:
            - revolutions_per_minute: The current speed of the mechanism
        '''
        return self._motor.get_velocity().value * 60

    def get_mechanism_speed_rad_per_sec(self) -> radians_per_second:
        '''
        Returns the current speed of the mechanism in radians per second

        Returns:
            - radians_per_second: The current speed of the mechanism
        '''
        return self._motor.get_velocity().value * tau

    def mechanism_at_target_speed(self) -> bool:
        '''
        Checks if the motor is at the target speed

        Returns:
            - bool: True if the motor is at the target speed, False otherwise
        '''
        if self._open_loop_request.output == 0.0 and self._closed_loop_request.velocity == 0.0:
            return True

        elif self._open_loop_request.output != 0.0:
            if self._closed_loop_request.velocity >= 0:
                return self._motor.get_velocity().value > self._closed_loop_request.velocity
            else:
                return self._motor.get_velocity().value < self._closed_loop_request.velocity

        # Convert RPS to RPM, then subtract the target speed and compare to the tolerance
        return abs(self._motor.get_velocity().value - self._closed_loop_request.velocity) < self._tolerance

    @override
    def set_power(self, power: float) -> None:
        '''
        Sets the power of the motor for testing purposes

        Parameters:
            - power (float): The power to set the motor to
        '''
        self._open_loop_request.output = power
        self._closed_loop_request.velocity = 0
    
    @override
    def print_diagnostics(self) -> None:
        '''
        Prints diagnostic information to Smart Dashboard
        '''
        SmartDashboard.putNumber(f"{self._name} Speed (RPM)", self.get_mechanism_speed())
        SmartDashboard.putNumber(f"{self._name} At Target RPM", self.mechanism_at_target_speed())
        super().print_diagnostics()

    @override
    def log_diagnostics(self) -> None:
        '''
        Logs diagnostic information to the data log
        '''
        if not self._logging_enabled:
            return

        self._speed_log.append(self.get_mechanism_speed())
        self._at_target_speed_log.append(self.mechanism_at_target_speed())

        super().log_diagnostics()