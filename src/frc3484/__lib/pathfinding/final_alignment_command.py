from typing import Callable

import commands2
from wpilib import Timer
from wpimath.geometry import Pose2d
from wpimath.units import inchesToMeters
from wpimath.kinematics import ChassisSpeeds

from pathplannerlib.controller import PathFollowingController, PathPlannerTrajectoryState

from .config import FinalAlignmentConfig

class FinalAlignmentCommand(commands2.Command):
    """
    A command that uses the drivetrain to do a precise alignment to a target pose
    Used by SC_Pathfinding to align the robot to the target pose,
        commonly after using pathfinding to roughly reach a pose
    
    Parameters:
        - target_pose (Pose2d): The target pose
        - drive_controller (PathFollowingController): The pathplanner drive controller to use for alignment
        - pose_supplier (Callable[[], Pose2d]): Function to get the robot's current pose
        - output (Callable[[ChassisSpeeds], None]): Function to output chassis speeds to the drivetrain
        - drivetrain_subsystem (Subsystem): The drivetrain subsystem for adding command requirements
    """
    def __init__(self, target_pose: Pose2d, drive_controller: PathFollowingController, pose_supplier: Callable[[], Pose2d], output: Callable[[ChassisSpeeds], None], drivetrain_subsystem: commands2.Subsystem, config: FinalAlignmentConfig | None = None) -> None:
        super().__init__()
        self.addRequirements(drivetrain_subsystem)
        self._pose_supplier: Callable[[], Pose2d] = pose_supplier
        self._output: Callable[[ChassisSpeeds], None] = output
        self._goal_state: PathPlannerTrajectoryState = PathPlannerTrajectoryState(pose=target_pose)

        self._drive_controller: PathFollowingController = drive_controller
        self._config: FinalAlignmentConfig = config if config else FinalAlignmentConfig()
        self._timer: Timer = Timer()

    @property
    def config(self) -> FinalAlignmentConfig:
        """
        Returns the configuration for the final alignment command

        Returns:
            - FinalAlignmentConfig: The configuration
        """
        return self._config
    @config.setter
    def config(self, config: FinalAlignmentConfig) -> None:
        """
        Sets the configuration for the final alignment command

        Parameters:
            - config (FinalAlignmentConfig): The new configuration
        """
        self._config = config

    def initialize(self) -> None:
        self._timer.reset()
        self._timer.start()

    def execute(self) -> None:
        self._output(
            self._drive_controller.calculateRobotRelativeSpeeds(
                self._pose_supplier(), 
                self._goal_state
            )
        )

    def end(self, interrupted: bool) -> None:
        self._output(ChassisSpeeds(0.0, 0.0, 0.0))
        self._timer.stop()
    
    def isFinished(self) -> bool:
        return self._timer.hasElapsed(self.config.TIMEOUT) or \
            (self._pose_supplier().translation().distance(self._goal_state.pose.translation()) < inchesToMeters(self.config.POSITION_TOLERANCE) and \
            abs(self._pose_supplier().rotation().degrees() - self._goal_state.pose.rotation().degrees()) < self.config.ROTATION_TOLERANCE)