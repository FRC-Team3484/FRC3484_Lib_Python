from phoenix6.units import rotation
from commands2 import Subsystem

from phoenix6.hardware import TalonFX, TalonFXS
from phoenix6.configs import CurrentLimitsConfigs, TalonFXConfiguration, TalonFXSConfiguration
from phoenix6.controls import Follower
from phoenix6.signals import InvertedValue, MotorArrangementValue, NeutralModeValue, MotorAlignmentValue
from wpilib import SmartDashboard, DataLogManager
from wpiutil.log import DataLog, DoubleLogEntry, BooleanLogEntry
from wpimath.units import turns, turns_per_second, volts

from ..datatypes.motion_datatypes import SC_MotorConfig

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
        self._name = motor_config.motor_name if motor_config.motor_name else motor_config.can_id
        

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

        # _ = SmartDashboard.putBoolean(f"{self._name} Diagnostics", False)
        self._motor_inverted = motor_config.inverted

    @property
    def device_id(self) -> int:
        return self._motor.device_id

    def periodic(self) -> None:
        '''
        Handles printing diagnostic information to Smart Dashboard
        '''
        # if SmartDashboard.getBoolean(f"{self._name} Diagnostics", False):
        #     self.print_diagnostics()
        #     self.log_diagnostics()
        pass

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
        motor_power = self._motor.get()
        supply_volage = self._motor.get_supply_voltage().value

        if abs(motor_power) > self.STALL_THRESHOLD and supply_volage > 0.01:
            return (self._motor.get_supply_current().value / (self._motor.get_motor_stall_current().value * supply_volage / 12.0)) / abs(motor_power)
        else:
            return 0
        
    def follow(self, motor: "PowerMotor") -> None:
        self._motor.set_control(Follower(motor.device_id, MotorAlignmentValue(self._motor_inverted)))
        

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
        _ = SmartDashboard.putNumber(f"Motor {self._name} Power (%)", self._motor.get() * 100)
        _ = SmartDashboard.putNumber(f"Motor {self._name} Stall Percentage", self.get_stall_percentage())
        _ = SmartDashboard.putNumber(f"Motor {self._name} Voltage (Volts)", self._motor.get_motor_voltage().value)
        _ = SmartDashboard.putBoolean(f"Motor {self._name} Stalled", self.get_stalled())

    def log_diagnostics(self, log: DataLog) -> None:
        stalled_log = BooleanLogEntry(log, f"Motor {self._name} Stalled")
        stalled_log.append(self.get_stalled())
        power_percent_log = DoubleLogEntry(log, f"Motor {self._name} Power (%)")
        power_percent_log.append(self._motor.get()*100)
        stall_percent_log = DoubleLogEntry(log, f"Motor {self._name} Stall Percentage")
        stall_percent_log.append(self.get_stall_percentage())
        voltage_log = DoubleLogEntry(log, f"Motor {self._name} Voltage (Volts)")
        voltage_log.append(self._motor.get_motor_voltage().value)

    def set_raw_voltage(self, voltage: volts) -> None:
        '''
        Sets the voltage of the motor

        Used for SysID routines

        Parameters:
            - voltage (volts): The voltage to set the motor to
        '''
        self._motor.setVoltage(voltage)

    def get_raw_voltage(self) -> volts:
        '''
        Returns the voltage of the motor

        Used for SysID routines

        Returns:
            - volts: The voltage of the motor
        '''
        return self._motor.get_motor_voltage().value

    def get_raw_position(self) -> turns:
        '''
        Returns the angular position of the motor

        Used for SysID routines

        Returns:
            - turns: The angular position of the motor
        '''
        return self._motor.get_position().value

    def get_raw_velocity(self) -> turns_per_second:
        '''
        Returns the angular velocity of the motor

        Used for SysID routines

        Returns:
            - turns_per_second: The angular velocity of the motor
        '''
        return self._motor.get_velocity().value
