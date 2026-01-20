from ..datatypes.pathing_datatypes import SC_CameraConfig as SC_CameraConfig, SC_CameraResults as SC_CameraResults
from photonlibpy.estimatedRobotPose import EstimatedRobotPose as EstimatedRobotPose
from photonlibpy.photonPoseEstimator import PoseStrategy
from photonlibpy.targeting import PhotonTrackedTarget as PhotonTrackedTarget
from photonlibpy.targeting.photonPipelineResult import PhotonPipelineResult as PhotonPipelineResult
from robotpy_apriltag import AprilTagField as AprilTagField
from typing import Iterable
from wpimath.geometry import Pose2d as Pose2d, Pose3d as Pose3d

class SC_Vision:
    def __init__(self, camera_configs: Iterable[SC_CameraConfig], april_tag_field: AprilTagField, pose_strategy: PoseStrategy, single_tag_st_devs: tuple[float, float, float], multi_tag_st_devs: tuple[float, float, float]) -> None: ...
    def get_camera_results(self, current_pose: Pose2d) -> list[SC_CameraResults]: ...
