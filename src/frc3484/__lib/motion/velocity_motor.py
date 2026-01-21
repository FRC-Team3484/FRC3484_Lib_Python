from typing import override

from wpilib import SmartDashboard

from phoenix6 import controls
from phoenix6.configs import CurrentLimitsConfigs, Slot0Configs

from ..datatypes.motion_datatypes import SC_LinearFeedForwardConfig, SC_PIDConfig, SC_MotorConfig, SC_LauncherSpeed
from .power_motor import PowerMotor


class VelocityMotor(PowerMotor):
    '''
    Creates a motor template class that represents a motor that can be set to a target speed

    Parameters:
        - motor_config (SC_MotorConfig): The configuration for the motor
        - current_config (SC_TemplateMotorCurrentConfig): Current limit settings for the motor
        - pid_config (SC_PIDConfig): The configuration for the PID controller
        - gear_ratio (float): The gear ratio of the motor
        - tolerance (float): The tolerance for the target speed to consider it reached
    '''
    STALL_LIMIT: float = 0.75
    STALL_THRESHOLD: float = 0.1

    def __init__(
        self, 
        motor_config: SC_MotorConfig, 
        pid_config: SC_PIDConfig, 
        feed_forward_config: SC_LinearFeedForwardConfig,
        gear_ratio: float, 
        tolerance: float
    ) -> None:
        super().__init__(motor_config)

        self._tolerance: float = tolerance
        self._gear_ratio: float = gear_ratio
        self._motor_name: str = str(self._motor.device_id)

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

    @override
    def periodic(self) -> None:
        '''
        Handles Smart Dashboard diagnostic information and actually controlling the motors
        '''
        if not SmartDashboard.getBoolean(f"{self._motor_name} Test Mode", False):
            if self._open_loop_request.output == 0.0 and self._closed_loop_request.velocity == 0.0:
                self._motor.set_control(self._open_loop_request.with_output(0))

            elif self._open_loop_request.output != 0.0:
                self._motor.set_control(self._open_loop_request)
            
            else:
                self._motor.set_control(self._closed_loop_request)

        if SmartDashboard.getBoolean(f"{self._motor_name} Diagnostics", False):
            self.print_diagnostics()
    
    def set_speed(self, speed: SC_LauncherSpeed) -> None:
        '''
        Sets the target speed for the motor

        Parameters:
            - speed (SC_TemplateMotorVelocityControl): The speed and power to set the motor to
        '''
        self._open_loop_request.output = speed.power
        self._closed_loop_request.velocity = (speed.speed * self._gear_ratio) / 60
        

    def at_target_speed(self) -> bool:
        '''
        Checks if the motor is at the target speed

        Returns:
            - bool: True if the motor is at the target speed, False otherwise
        '''
        if self._open_loop_request.output == 0.0 and self._closed_loop_request.velocity == 0.0:
            return True

        elif self._open_loop_request.output != 0.0:
            return (self._motor.get_velocity().value - self._closed_loop_request.velocity) * (1 if self._closed_loop_request.velocity >= 0 else -1) > 0

        # Convert RPS to RPM, then subtract the target speed and compare to the tolerance
        return abs(self._motor.get_velocity().value - self._closed_loop_request.velocity) < self._tolerance

    @override
    def set_power(self, power: float) -> None:
        '''
        Sets the power of the motor for testing purposes

        Parameters:
            - power (float): The power to set the motor to
        '''
        # TODO: Have a boolean for testing mode to disable PID and feed forward
        # TODO: Should this really override the set_speed method from PowerMotor?
        self._open_loop_request.output = power
        self._closed_loop_request.velocity = 0
    
    @override
    def print_diagnostics(self) -> None:
        '''
        Prints diagnostic information to Smart Dashboard
        '''
        _ = SmartDashboard.putNumber(f"{self._motor_name} Speed (RPM)", self._motor.get_velocity().value * 60)
        _ = SmartDashboard.putNumber(f"{self._motor_name} At Target RPM", self.at_target_speed())
        super().print_diagnostics()