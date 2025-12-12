from enum import Enum
from typing import override

from wpilib import Timer, SmartDashboard
from wpimath.units import degrees, degrees_per_second
from wpimath.controller import PIDController, SimpleMotorFeedforwardMeters
from wpimath.trajectory import TrapezoidProfile

from phoenix6.hardware import CANcoder
from phoenix6.configs import ExternalFeedbackConfigs, FeedbackConfigs, TalonFXSConfiguration, TalonFXConfiguration
from phoenix6.signals import ExternalFeedbackSensorSourceValue, FeedbackSensorSourceValue

from ..motion.power_motor import PowerMotor
from ..datatypes.motion_datatypes import SC_AngularFeedForwardConfig, SC_LinearFeedForwardConfig, SC_PIDConfig, SC_MotorConfig, SC_TrapezoidConfig

class State(Enum):
    POWER = 0
    POSITION = 1

class AngularPositionMotor(PowerMotor):
    '''
    Defines a base motor class for angular position control

    Parameters:
        motor_config: SC_TemplateMotorConfig
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
            feed_forward_config: SC_AngularFeedForwardConfig | SC_LinearFeedForwardConfig,
            trapezoid_config: SC_TrapezoidConfig,
            angle_tolerance: degrees,
            gear_ratio: float = 1.0,
            external_encoder: CANcoder | None = None
        ) -> None:
        super().__init__(motor_config)

        # Set up variables
        self._state: State = State.POWER

        self._pid_controller: PIDController = PIDController(pid_config.Kp, pid_config.Ki, pid_config.Kd)
        self._feed_forward_controller: SimpleMotorFeedforwardMeters = SimpleMotorFeedforwardMeters(feed_forward_config.S, feed_forward_config.V, feed_forward_config.A)
        self._motor_name: str = str(self._motor.device_id)

        self._trapezoid: TrapezoidProfile = TrapezoidProfile(TrapezoidProfile.Constraints(trapezoid_config.max_velocity, trapezoid_config.max_acceleration))
        self._trapezoid_timer: Timer = Timer()

        self._encoder: CANcoder | None = external_encoder

        self._initial_state: TrapezoidProfile.State = TrapezoidProfile.State(0.0, 0.0)
        self._target_state: TrapezoidProfile.State = TrapezoidProfile.State(0.0, 0.0)

        self._previous_velocity: degrees_per_second = 0

        self._gear_ratio: float = gear_ratio
        self._angle_tolerance: degrees = angle_tolerance

        # Set up motor

        # If the motor_type is minion, it needs a talon FXS controller to be able to set the correct commutation
        # There is no communtation for the falcon, so use a talon FX controller instead
        # The portion for the external encoder is here, but the rest of the configuration is in the PowerMotor class
        if type(self._motor_config) is TalonFXSConfiguration:
            if self._encoder is not None:
                self._motor_config.external_feedback = ExternalFeedbackConfigs() \
                    .with_feedback_remote_sensor_id(self._encoder.device_id) \
                    .with_external_feedback_sensor_source(ExternalFeedbackSensorSourceValue.REMOTE_CANCODER)

        elif type(self._motor_config) is TalonFXConfiguration:
            if self._encoder is not None:
                self._motor_config.feedback = FeedbackConfigs() \
                    .with_feedback_remote_sensor_id(self._encoder.device_id) \
                    .with_feedback_sensor_source(FeedbackSensorSourceValue.REMOTE_CANCODER)
        else:
            raise ValueError(f"Invalid motor type: {motor_config.motor_type}")

        _ = self._motor.configurator.apply(self._motor_config)        

        self._trapezoid_timer.start()

    @override
    def periodic(self) -> None:
        '''
        Handles controlling the motors in position mode and printing diagnostics
        '''
        if self._state == State.POSITION:
            current_state = self._trapezoid.calculate(self._trapezoid_timer.get(), self._initial_state, self._target_state)
            feed_forward = self._feed_forward_controller.calculate(self._previous_velocity, current_state.velocity)
            pid = self._pid_controller.calculate(self.get_angle(), current_state.position)

            self._motor.setVoltage(pid + feed_forward)
            self._previous_velocity = current_state.velocity

        if SmartDashboard.getBoolean(f"{self._motor_name} Diagnostics", defaultValue=False):
            self.print_diagnostics()

    def at_target_angle(self) -> bool:
        '''
        Returns whether the motor is at the target angle or not

        Returns:
            - bool: True if the motor is at the target angle, False otherwise
        '''
        return abs(self._target_state.position - self.get_angle()) < self._angle_tolerance

    def get_angle(self) -> degrees:
        '''
        Returns the current angle of the motor

        Returns:
            - degrees: The current angle of the motor
        '''
        return self._motor.get_position().value / self._gear_ratio

    def get_velocity(self) -> degrees_per_second:
        '''
        Returns the current velocity of the motor

        Returns:
            - degrees_per_second: The current velocity of the motor
        '''
        return self._motor.get_velocity().value / self._gear_ratio

    def set_power(self, power: float) -> None:
        '''
        Sets the power of the motor

        Parameters:
            - power (float): The power to set the motor to
        '''
        self._state = State.POWER
        self._motor.set(power)

    def set_target_angle(self, angle: degrees) -> None:
        '''
        Sets the target angle of the motor

        Parameters:
            - angle (degrees): The angle to set the motor to
        '''
        self._state = State.POSITION
        
        if angle != self._target_state.position:
            self._target_state = TrapezoidProfile.State(angle, 0)
            self._initial_state = TrapezoidProfile.State(self.get_angle(), self.get_velocity())

            self._trapezoid_timer.reset()

    @override
    def print_diagnostics(self) -> None:
        '''
        Prints diagnostic information to Smart Dashboard
        '''
        _ = SmartDashboard.putNumber(f"{self._motor_name} Angle (degrees)", self.get_angle())
        _ = SmartDashboard.putNumber(f"{self._motor_name} Velocity", self.get_velocity())
        _ = SmartDashboard.putBoolean(f"{self._motor_name} At Target Angle", self.at_target_angle())
        super().print_diagnostics()