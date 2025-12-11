from typing import Iterable

from wpimath.geometry import Pose2d, Pose3d
from robotpy_apriltag import AprilTagFieldLayout

def get_april_tag_poses(april_tag_ids: Iterable[int], layout: AprilTagFieldLayout) -> list[Pose2d]:
    """
    Returns the poses of april tags by id

    Parameters:
        - april_tag_ids (list[int]): List of april tag ids
        - layout (AprilTagFieldLayout): The april tag field layout
    Returns:
        - list[Pose2d]: The list of poses based on the specified ids
    """
    poses: list[Pose2d] = []

    for id in april_tag_ids:
        pose: Pose3d | None = layout.getTagPose(id)
        if pose is not None:
            poses.append(pose.toPose2d())
    
    return poses

def apply_offset_to_pose(pose: Pose2d, offset: Pose2d) -> Pose2d:
    """
    Applies an offset to a pose

    Parameters:
        - pose (Pose2d): The pose to apply the offset to
        - offset (Pose2d): The offset to apply

    Returns:
        - Pose2d: The resulting pose
    """
    return Pose2d(pose.translation() + offset.translation().rotateBy(pose.rotation()), pose.rotation() + offset.rotation())

def apply_offsets_to_poses(poses: Iterable[Pose2d], offsets: Iterable[Pose2d]) -> list[Pose2d]:
    """
    Applies a list of offsets to a list of poses  
    Will return the number of offsets equal to poses times offsets  
    For example, if two poses and two offsets are provided, four poses will be returned  
    This iterates through offsets first, then poses: p1o1, p1o2, p2o1, p2o2...

    Parameters:
        - poses (list[Pose2d]): The poses to apply the offsets to
        - offsets (list[Pose2d]): The offsets to apply

    Returns:
        - list[Pose2d]: The resulting poses
    """
    return [apply_offset_to_pose(pose, offset) for pose in poses for offset in offsets]

def get_nearest_pose(current_position: Pose2d, poses: Iterable[Pose2d]) -> Pose2d:
    """
    Returns the nearest pose to the robot's current position

    Parameters:
        - current_position (Pose2d): The robot's current position
        - poses (list[Pose2d]): The list of poses to find the nearest pose from

    Returns:
        - Pose2d: The nearest pose
    """
    if not type(poses) == list:
        poses = list(poses)
    return current_position.nearest(poses)