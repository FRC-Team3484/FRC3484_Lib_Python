from typing import override

import commands2
from wpimath.geometry import Pose2d

from pathplannerlib.controller import PathFollowingController, PathPlannerTrajectoryState

from src.subsystems.drivetrain_subsystem import DrivetrainSubsystem
from src.FRC3484_Lib.pathfinding.pathfinding_constants import FinalAlignmentCommandConstants

class FinalAlignmentCommand(commands2.Command):
    """
    A command that uses the drivetrain to do a precise alignment to a target pose
    Used by SC_Pathfinding to align the robot to the target pose,
        commonly after using pathfinding to roughly reach a pose
    
    Parameters:
        - drivetrain_subsystem (DrivetrainSubsystem): The drivetrain subsystem
        - target_pose (Pose2d): The target pose
    """
    def __init__(self, drivetrain_subsystem: DrivetrainSubsystem, target_pose: Pose2d, drive_controller: PathFollowingController) -> None:
        super().__init__()
        self.addRequirements(drivetrain_subsystem)
        self.drivetrain_subsystem: DrivetrainSubsystem = drivetrain_subsystem
        self.goal_state: PathPlannerTrajectoryState = PathPlannerTrajectoryState(pose=target_pose)

        self.drive_controller: PathFollowingController = drive_controller
        self.counter: int = 0

    @override
    def initialize(self) -> None:
        self.counter = 0

    @override
    def execute(self) -> None:
        self.counter += 1

        self.drivetrain_subsystem.drive_robotcentric(
            self.drive_controller.calculateRobotRelativeSpeeds(
                self.drivetrain_subsystem.get_pose(), 
                self.goal_state
            ), 
            open_loop=False
        )

    @override
    def end(self, interrupted: bool) -> None:
        self.drivetrain_subsystem.stop_motors()
    
    @override
    def isFinished(self) -> bool:
        return self.counter >= FinalAlignmentCommandConstants.FINAL_ALIGN_EXIT or \
            (self.drivetrain_subsystem.get_pose().translation().distance(self.goal_state.pose.translation()) < FinalAlignmentCommandConstants.FINAL_POSE_TOLERANCE and \
            abs(self.drivetrain_subsystem.get_pose().rotation().degrees() - self.goal_state.pose.rotation().degrees()) < FinalAlignmentCommandConstants.FINAL_ROTATION_TOLERANCE)