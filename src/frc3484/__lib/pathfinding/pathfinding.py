from typing import Callable, Iterable

import commands2
from wpimath.geometry import Pose2d
from wpimath.kinematics import ChassisSpeeds
from wpimath.units import inches, inchesToMeters

from pathplannerlib.auto import AutoBuilder
from pathplannerlib.controller import PathFollowingController
from pathplannerlib.path import PathPlannerPath, GoalEndState

from .config import PathfindingConfig, FinalAlignmentConfig
from .final_alignment_command import FinalAlignmentCommand
from ..datatypes.pathing_datatypes import SC_ApriltagTarget

class SC_Pathfinding:
    """
    A library for handling the pathfinding of the robot

    Can do april tag math, and return commands for pathfinding

    Parameters:
        - drivetrain_subsystem (Subsystem): The drivetrain subsystem for adding command requirements
        - pose_supplier (Callable[[], Pose2d]): Function to get the robot's current pose
        - output (Callable[[ChassisSpeeds], None]): Function to output chassis speeds to the drivetrain
        - alignment_controller (PathFollowingController): The controller to use for final alignment
    """
    def __init__(self, drivetrain_subsystem: commands2.Subsystem, pose_supplier: Callable[[], Pose2d], output: Callable[[ChassisSpeeds], None], alignment_controller: PathFollowingController) -> None:
        self._drivetrain_subsystem: commands2.Subsystem = drivetrain_subsystem
        self._pose_supplier: Callable[[], Pose2d] = pose_supplier
        self._output: Callable[[ChassisSpeeds], None] = output
        self._alignment_controller: PathFollowingController = alignment_controller
        self.config: PathfindingConfig = PathfindingConfig()
        self.alignment_config: FinalAlignmentConfig = FinalAlignmentConfig()

    def get_final_alignment_command(self, target: Pose2d) -> commands2.Command:
        """
        Returns a command to align the robot to a target pose

        Parameters:
            - target (Pose2d): The target pose to align to
            - defer (bool): Whether to defer the command

        Returns:
            - Command: The command to align to the target
        """
        return FinalAlignmentCommand(target, self._alignment_controller, self._pose_supplier, self._output, self._drivetrain_subsystem, self.alignment_config)

    def get_near_pose_command(self, target: Pose2d, distance: inches) -> commands2.Command:
        """
        Returns a command that does nothing and waits until the robot is within a distance, then exits
        Intended to be used in parallel with a pathing command so once the robot is close to its end position, 
            the command group will exit and the final alignment command can take over

        Parameters:
            - target (Pose2d): The target pose to align to
            - distance (inches): The distance to wait before exiting

        Returns:
            - Command: The command to align to the target
        """
        return commands2.WaitUntilCommand(lambda: self._pose_supplier().translation().distance(target.translation()) < inchesToMeters(distance))
    
    def get_pathfollow_command(self, start_pose: Pose2d, target: Pose2d, intermediate_points: Iterable[Pose2d] | None = None) -> commands2.Command:
        """
        Returns a command that drives from start pose to target pose, without opstacle avoidance and optionally through intermediate points

        Parameters:
            - start_pose (Pose2d): The starting pose
            - target (Pose2d): The target pose
            - intermediate_points (list[Pose2d] | None): Optional intermediate points to drive through

        Returns:
            - Command: The command to drive through all the points
        """
        poses: list[Pose2d] = [start_pose]
        if intermediate_points is not None:
            poses.extend(intermediate_points)
        poses.append(target)

        path = PathPlannerPath(
            PathPlannerPath.waypointsFromPoses(poses),
            self.config.PATH_CONSTRAINTS,
            None,
            GoalEndState(0, target.rotation())
        )

        path.preventFlipping = True

        return AutoBuilder.followPath(path)

    
    def get_pathfind_command(self, target: Pose2d) -> commands2.Command:
        """
        Returns a command that drives to target pose, avoiding obstacles.  
        This command is NOT safe for use in autonomous, use pathfind_to_pose instead

        Parameters:
            - target (Pose2d): The target pose

        Returns:
            - Command: The command to drive to the target
        """
        return AutoBuilder.pathfindToPose(target, self.config.PATH_CONSTRAINTS, 0.0)
    
    def pathfind_to_pose(self, target_pose: Pose2d, safe_distance: inches = 999, defer: bool = False) -> commands2.Command:
        """
        Returns a command that creates a path to drive to the given target pose.
        This command is safe for use in autonomous

        Parameters:
            - target_pose (Pose2d): The target pose to drive to
            - defer (bool): Whether to defer the command

        Returns:
            - Command: The command to drive to the target pose
        """
        if defer: return commands2.DeferredCommand(lambda: self.pathfind_to_pose(target_pose, defer=False))

        start_pose: Pose2d = self._pose_supplier()
        if target_pose.relativeTo(start_pose).translation().norm() < inchesToMeters(safe_distance):
            drive_command: commands2.Command = self.get_pathfollow_command(start_pose, target_pose)
        else:
            drive_command: commands2.Command = self.get_pathfind_command(target_pose)

        return commands2.SequentialCommandGroup(
            commands2.ParallelRaceGroup(
                drive_command,
                self.get_near_pose_command(target_pose, inchesToMeters(self.config.FINAL_ALIGNMENT_DISTANCE))
            ),
            self.get_final_alignment_command(target_pose)
        )

    def pathfind_to_target(self, target: SC_ApriltagTarget, defer: bool = False) -> commands2.Command:
        """
        Returns a command that creates a path to drive to the nearest point on the given target.  
        This command is safe for use in autonomous

        Parameters:
            - target (SC_ApriltagTarget): The april tag target to drive to
            - start_pose (Pose2d | None): The starting pose. If None, will use the robot's current pose.

        Returns:
            - Command: The command to drive to the nearest point on the target
        """
        return self.pathfind_to_pose(target.get_nearest(self._pose_supplier()), safe_distance=target.safe_distance, defer=defer)