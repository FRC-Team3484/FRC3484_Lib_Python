from typing import final, override

from wpilib import DataLogManager, SmartDashboard
from wpimath.units import degrees, inches, feet_per_second, inchesToMeters, degreesToRadians, radiansToDegrees
from wpiutil.log import BooleanLogEntry, DoubleLogEntry
inches_per_second = float

from phoenix6.hardware import CANcoder

from .angular_pos_motor import AngularPositionMotor
from ..datatypes.motion_datatypes import SC_PIDConfig, SC_MotorConfig, SC_LinearTrapezoidConfig, SC_AngularTrapezoidConfig, SC_LinearFeedForwardConfig, SC_AngularFeedForwardConfig

@final
class LinearPositionMotor(AngularPositionMotor):
    '''
    Defines a base motor class for linear position control

    Parameters:
        motor_config: SC_MotorConfig
        current_config: SC_TemplateMotorCurrentConfig
        pid_config: SC_PIDConfig
        feed_forward_config: SC_LinearFeedForwardConfig
        trapezoid_config: SC_TemplateMotorTrapezoidConfig
        position_tolerance: feet
        gear_ratio: float
        logging_enabled: bool
        external_encoder: CANcoder | None = None
    '''
    STALL_LIMIT: float = 0.75
    STALL_THRESHOLD: float = 0.1

    def __init__(
            self,
            motor_config: SC_MotorConfig,
            pid_config: SC_PIDConfig,
            feed_forward_config: SC_LinearFeedForwardConfig,
            trapezoid_config: SC_LinearTrapezoidConfig,
            position_tolerance: inches,
            pulley_radius: inches,
            gear_ratio: float,
            logging_enabled: bool,
            external_encoder: CANcoder | None = None
        ) -> None:

        super().__init__(
            motor_config=motor_config, 
            pid_config=pid_config, 
            feed_forward_config=SC_AngularFeedForwardConfig(
                feed_forward_config.G,
                feed_forward_config.S,
                feed_forward_config.V * inchesToMeters(pulley_radius),
                feed_forward_config.A * inchesToMeters(pulley_radius)
                ), 
            trapezoid_config=SC_AngularTrapezoidConfig(
                radiansToDegrees(trapezoid_config.max_velocity * 12 / pulley_radius),
                radiansToDegrees(trapezoid_config.max_acceleration * 12 / pulley_radius)
                ), 
            angle_tolerance=radiansToDegrees(position_tolerance/pulley_radius), 
            gear_ratio=gear_ratio,
            logging_enabled=logging_enabled,
            external_encoder=external_encoder
        )

        self._pulley_radius: inches = pulley_radius

        if self._logging_enabled:
            self._position_log = DoubleLogEntry(DataLogManager.getLog(), f"/motors/{self._name}/position_inches")
            self._velocity_log = DoubleLogEntry(DataLogManager.getLog(), f"/motors/{self._name}/velocity_feet_per_second")
            self._at_target_position_log = BooleanLogEntry(DataLogManager.getLog(), f"/motors/{self._name}/at_target_position")

    def _mechanism_to_angular(self, position: inches) -> degrees:
        return radiansToDegrees(position / self._pulley_radius)
    def _angular_to_mechanism(self, angle: degrees) -> inches:
        return degreesToRadians(angle) * self._pulley_radius
        
    @override
    def at_target_position(self) -> bool:
        '''
        Returns whether the mechanism is at the target position or not

        Returns:
            - bool: True if the mechanism is at the target position, False otherwise
        '''
        return super().at_target_position()

    @override
    def get_position(self) -> inches:
        '''
        Returns the current position of the mechanism

        Returns:
            - inches: The current linear position of the mechanism
        '''
        return self._angular_to_mechanism(super().get_position())

    @override
    def get_velocity(self) -> feet_per_second:
        '''
        Returns the current velocity of the mechanism

        Returns:    
            - feet_per_second: The current velocity of the mechanism
        '''
        return self._angular_to_mechanism(super().get_velocity()) / 12.0
    
    @override
    def set_target_position(self, position: inches) -> None:
        '''
        Sets the target position of the mechanism

        Parameters:
            - position (inches): The linear position to set the mechanism to
        '''
        super().set_target_position(self._mechanism_to_angular(position))

    @override
    def print_diagnostics(self) -> None:
        '''
        Prints diagnostic information to Smart Dashboard
        '''
        SmartDashboard.putNumber(f"{self._name} Position (inches)", self.get_position())
        SmartDashboard.putNumber(f"{self._name} Velocity (feet/s)", self.get_velocity())
        SmartDashboard.putBoolean(f"{self._name} At Target Position", self.at_target_position())
        super().print_diagnostics()

    @override
    def log_diagnostics(self) -> None:
        if not self._logging_enabled:
            return
        
        self._position_log.append(self.get_position())
        self._velocity_log.append(self.get_velocity())
        self._at_target_position_log.append(self.at_target_position())
        
        super().log_diagnostics()

    @override
    def set_position(self, position: inches) -> None:
        '''
        Sets the position of the mechanism in inches

        Parameters:
            - position (inches): The current linear position of the mechanism
        '''
        return super().set_position(self._mechanism_to_angular(position))