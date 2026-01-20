from ..pose_manipulation.pose_manipulation import *
from dataclasses import dataclass
from robotpy_apriltag import AprilTagField as AprilTagField
from typing import Iterable
from wpilib import DriverStation
from wpimath.geometry import Pose2d as Pose2d, Transform3d as Transform3d
from wpimath.units import inches as inches, seconds as seconds

@dataclass(frozen=True)
class SC_CameraConfig:
    name: str
    position: Transform3d
    enabled: bool = ...

@dataclass(frozen=True)
class SC_CameraResults:
    vision_measurement: Pose2d
    timestamp: seconds
    standard_deviation: tuple[float, float, float]

class SC_ApriltagTarget:
    def __init__(self, apriltag_ids: Iterable[int], offsets: Iterable[Pose2d], safe_distance: inches, field: AprilTagField, red_apriltag_ids: Iterable | None = None) -> None: ...
    @property
    def targets(self) -> list[Pose2d]: ...
    @property
    def safe_distance(self) -> inches: ...
    def get_targets_for_alliance(self, alliance: DriverStation.Alliance) -> list[Pose2d]: ...
    def get_nearest(self, current_position: Pose2d) -> Pose2d: ...
