from dataclasses import dataclass
from typing import Iterable

from wpimath.units import \
    seconds, \
    inches

from wpilib import DriverStation
from wpimath.geometry import Transform3d, Pose2d
from robotpy_apriltag import AprilTagField, AprilTagFieldLayout

from ..pose_manipulation.pose_manipulation import *

'''
Vision, Pathfinding, and Field Datatypes
'''

@dataclass(frozen=True)
class SC_CameraConfig:
    name: str
    position: Transform3d
    enabled: bool = True

@dataclass(frozen=True)
class SC_CameraResults:
    vision_measurement: Pose2d
    timestamp: seconds
    standard_deviation: tuple[float, float, float]

class SC_ApriltagTarget:
    def __init__(self, apriltag_ids: Iterable[int], offsets: Iterable[Pose2d], safe_distance: inches, field: AprilTagField, red_apriltag_ids: Iterable | None = None) -> None:
        """
        A class for holding all information needed to pathfind to a field element

        Target poses are calculated by applying offsets to april tag poses

        Positive X is in front of the april tag, positive Y is to the right of the april tag (when facing the tag), and

        0 degrees rotation is facing away from the april tag, positive rotation is counter-clockwise

        Parameters:
            - apriltag_ids (Iterable[int]): April tag ids that can be used by both alliances
            - offsets (Iterable[Pose2d]): The offsets to apply to the april tag poses
            - safe_distance (inches): The safe distance to maintain from the target
            - field (AprilTagField): The field layout to use
            - red_apriltag_ids (Iterable[int] | None): If provided, these april tag ids will be used for the red alliance and the apriltag_ids will be used for the blue alliance
        """
        field_layout = AprilTagFieldLayout.loadField(field)
        blue_ids = list(apriltag_ids)
        red_ids = list(red_apriltag_ids) if red_apriltag_ids is not None else blue_ids

        self._target_poses: dict[DriverStation.Alliance, list[Pose2d]] = {
            DriverStation.Alliance.kBlue: apply_offsets_to_poses(
                get_april_tag_poses(blue_ids, field_layout),
                offsets
            ),
            DriverStation.Alliance.kRed: apply_offsets_to_poses(
                get_april_tag_poses(red_ids, field_layout),
                offsets
            )
        }

        self._safe_distance: inches = safe_distance

    @property
    def _alliance(self) -> DriverStation.Alliance:
        """
        Returns the current alliance of the robot

        Returns:
            - DriverStation.Alliance: The current alliance
        """
        alliance = DriverStation.getAlliance()
        if alliance is None:
            alliance = DriverStation.Alliance.kBlue
        return alliance

    @property
    def targets(self) -> list[Pose2d]:
        """
        Returns the target poses for the current alliance
        Returns:
            - list[Pose2d]: The target poses for the current alliance
        """
        return self._target_poses[self._alliance]
    
    @property
    def safe_distance(self) -> inches:
        """
        Returns the safe distance to maintain from the target

        Returns:
            - inches: The safe distance
        """
        return self._safe_distance

    def get_targets_for_alliance(self, alliance: DriverStation.Alliance) -> list[Pose2d]:
        """
        Returns the target poses for the specified alliance

        Parameters:
            - alliance (DriverStation.Alliance | None): The alliance to use. If None, will use the current alliance. If there's no current alliance, will default to blue

        Returns:
            - list[Pose2d]: The target poses for the specified alliance
        """
        if alliance is None:
            alliance = self._alliance
        return self._target_poses[alliance]


    def get_nearest(self, current_position: Pose2d) -> Pose2d:
        """
        Returns the nearest target pose to the robot's current position

        Parameters:
            - current_position (Pose2d): The robot's current position

        Returns:
            - Pose2d: The nearest target pose
        """
        return get_nearest_pose(current_position, self.targets)