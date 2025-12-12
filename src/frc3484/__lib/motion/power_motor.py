from commands2 import Subsystem

from phoenix6.hardware import TalonFX, TalonFXS
from phoenix6.configs import CurrentLimitsConfigs, TalonFXConfiguration, TalonFXSConfiguration
from phoenix6.signals import InvertedValue, MotorArrangementValue, NeutralModeValue
from wpilib import SmartDashboard

from ..datatypes import SC_MotorConfig

class PowerMotor(Subsystem):
    '''
    Creates a motor template class that can be used to create a 
        base motor that simply powers forwards or backwards at a given power

    Parameters:
        - motor_config (SC_MotorConfig): The configuration for the motor
        - current_config (SC_TemplateMotorCurrentConfig): Current limit settings for the motor
    '''
    STALL_LIMIT: float = 0.75
    STALL_THRESHOLD: float = 0.1

    def __init__(
            self, 
            motor_config: SC_MotorConfig
        ) -> None:
        super().__init__()
        
        self._motor: TalonFX | TalonFXS
        self._motor_config: TalonFXConfiguration | TalonFXSConfiguration

        

        # If the motor_type is minion, it needs a talon FXS controller to be able to set the correct commutation
        # There is no communtation for the falcon, so use a talon FX controller instead
        if motor_config.motor_type == "minion":
            self._motor = TalonFXS(motor_config.can_id, motor_config.can_bus_name)

            self._motor_config = TalonFXSConfiguration()

            self._motor_config.commutation.motor_arrangement = MotorArrangementValue.MINION_JST

        elif motor_config.motor_type == "falcon":
            self._motor = TalonFX(motor_config.can_id, motor_config.can_bus_name)

            self._motor_config = TalonFXConfiguration()
        else:
            raise ValueError(f"Invalid motor type: {motor_config.motor_type}")

        self._motor_config.motor_output.inverted = InvertedValue(motor_config.inverted)

        self._motor_config.motor_output.neutral_mode = motor_config.neutral_mode

        self._motor_config.current_limits = CurrentLimitsConfigs() \
            .with_supply_current_limit_enable(motor_config.current_limit_enabled) \
            .with_supply_current_limit(motor_config.current_limit) \
            .with_supply_current_lower_limit(motor_config.current_threshold) \
            .with_supply_current_lower_time(motor_config.current_time)

        _ = self._motor.configurator.apply(self._motor_config)

        _ = SmartDashboard.putBoolean(f"{self._motor.device_id} Diagnostics", False)

    def periodic(self) -> None:
        '''
        Handles printing diagnostic information to Smart Dashboard
        '''
        if SmartDashboard.getBoolean(f"{self._motor.device_id} Diagnostics", False):
            self.print_diagnostics()

    def set_power(self, power: float) -> None:
        '''
        Sets the power of the motor

        Parameters:
            - power (float): The power to set the motor to
        '''
        self._motor.set(power)

    def set_brake_mode(self) -> None:
        '''
        Sets the motor to brake mode
        '''
        self._motor_config.motor_output.neutral_mode = NeutralModeValue.BRAKE
        _ = self._motor.configurator.apply(self._motor_config)

    def set_coast_mode(self) -> None:
        '''
        Sets the motor to coast mode
        '''
        self._motor_config.motor_output.neutral_mode = NeutralModeValue.COAST
        _ = self._motor.configurator.apply(self._motor_config)

    def get_stall_percentage(self) -> float:
        '''
        Returns the percentage of stall current being drawn by the motor

        Returns:
            - float: The percentage of stall current being drawn by the motor
        '''
        if abs(self._motor.get()) > self.STALL_THRESHOLD:
            return (self._motor.get_supply_current().value / (self._motor.get_motor_stall_current().value * self._motor.get_supply_voltage().value / 12.0)) / abs(self._motor.get())
        else:
            return 0

    def get_stalled(self) -> bool:
        '''
        Returns whether the motor is stalled or not

        Returns:
            - bool: True if the motor is stalled, False otherwise
        '''
        return self.get_stall_percentage() > self.STALL_LIMIT
    
    def print_diagnostics(self) -> None:
        '''
        Prints diagnostic information to Smart Dashboard
        '''
        _ = SmartDashboard.putNumber(f"Motor {self._motor.device_id} Power (%)", self._motor.get() * 100)
        _ = SmartDashboard.putNumber(f"Motor {self._motor.device_id} Stall Percentage", self.get_stall_percentage())
        _ = SmartDashboard.putBoolean(f"Motor {self._motor.device_id} Stalled", self.get_stalled())