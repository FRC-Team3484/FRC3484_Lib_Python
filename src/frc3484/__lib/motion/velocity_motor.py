from typing import override

from wpilib import SmartDashboard
from wpimath.controller import PIDController, SimpleMotorFeedforwardMeters
from wpimath.units import volts

from src.FRC3484_Lib.SC_Datatypes import SC_LinearFeedForwardConfig, SC_PIDConfig, SC_MotorConfig, SC_CurrentConfig, SC_VelocityControl
from src.FRC3484_Lib.motor_templates.power_motor import PowerMotor


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
        current_config: SC_CurrentConfig, 
        pid_config: SC_PIDConfig, 
        feed_forward_config: SC_LinearFeedForwardConfig,
        gear_ratio: float, 
        tolerance: float
    ) -> None:
        super().__init__(motor_config, current_config)

        self._pid_controller: PIDController = PIDController(pid_config.Kp, pid_config.Ki, pid_config.Kd)
        self._feed_forward_controller: SimpleMotorFeedforwardMeters = SimpleMotorFeedforwardMeters(feed_forward_config.S, feed_forward_config.V, feed_forward_config.A)

        self._target_speed: SC_VelocityControl = SC_VelocityControl(0.0, 0.0)

        self._tolerance: float = tolerance
        self._gear_ratio: float = gear_ratio
        self._motor_name: str = motor_config.motor_name

    @override
    def periodic(self) -> None:
        '''
        Handles Smart Dashboard diagnostic information and actually controlling the motors
        '''
        if not SmartDashboard.getBoolean(f"{self._motor_name} Test Mode", False):
            if self._target_speed.power == 0.0 and self._target_speed.speed == 0.0:
                self._pid_controller.reset(0)
                self._motor.setVoltage(0)

            elif self._target_speed.power != 0.0:
                self._motor.set(self._target_speed.power)
            
            else:
                pid: volts = self._pid_controller.calculate(self._motor.get_velocity().value, self._target_speed.speed)
                feed_forward: volts = self._feed_forward_controller.calculate(self._motor.get_velocity().value, self._target_speed.speed)
                self._motor.setVoltage(pid + feed_forward)

        if SmartDashboard.getBoolean(f"{self._motor_name} Diagnostics", False):
            self.print_diagnostics()
    
    def set_speed(self, speed: SC_VelocityControl) -> None:
        '''
        Sets the target speed for the motor

        Parameters:
            - speed (SC_TemplateMotorVelocityControl): The speed and power to set the motor to
        '''
        self._target_speed = SC_VelocityControl(speed.speed * self._gear_ratio, speed.power)

    def at_target_speed(self) -> bool:
        '''
        Checks if the motor is at the target speed

        Returns:
            - bool: True if the motor is at the target speed, False otherwise
        '''
        if self._target_speed.power == 0.0 and self._target_speed.speed == 0.0:
            return True

        elif self._target_speed.power != 0.0:
            return (self._motor.get() - self._target_speed.speed) * (1 if self._target_speed.speed >= 0 else -1) > 0

        # Convert RPS to RPM, then subtract the target speed and compare to the tolerance
        return abs((self._motor.get_velocity().value * 60) - self._target_speed.speed) < self._tolerance

    @override
    def set_power(self, power: float) -> None:
        '''
        Sets the power of the motor for testing purposes

        Parameters:
            - power (float): The power to set the motor to
        '''
        # TODO: Have a boolean for testing mode to disable PID and feed forward
        # TODO: Should this really override the set_speed method from PowerMotor?
        self._target_speed = SC_VelocityControl(0.0, power)
    
    @override
    def print_diagnostics(self) -> None:
        '''
        Prints diagnostic information to Smart Dashboard
        '''
        _ = SmartDashboard.putNumber(f"{self._motor_name} Speed (RPM)", self._motor.get_velocity().value * 60)
        _ = SmartDashboard.putNumber(f"{self._motor_name} At Target RPM", self.at_target_speed())
        super().print_diagnostics()