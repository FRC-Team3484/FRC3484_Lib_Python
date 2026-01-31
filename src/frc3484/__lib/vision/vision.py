from photonlibpy.targeting.multiTargetPNPResult import MultiTargetPNPResult


import sys
from typing import Iterable

from phoenix6.controls import music_tone
from wpimath.geometry import Pose2d, Pose3d
from wpimath.units import meters
from robotpy_apriltag import AprilTagField, AprilTagFieldLayout

from photonlibpy import EstimatedRobotPose, PhotonCamera
from photonlibpy.targeting import PhotonTrackedTarget
from photonlibpy.targeting.photonPipelineResult import PhotonPipelineResult
from photonlibpy.photonPoseEstimator import PhotonPoseEstimator

from ..datatypes.pathing_datatypes import SC_CameraConfig, SC_CameraResults


class SC_Vision:
    """
    A class for handling vision processing

    Will return the estimated pose of the robot, based on the given camera configs

    Parameters:
        - camera_configs (list[SC_CameraConfig]): A list of camera configs
        - april_tag_layout (AprilTagFieldLayout): The april tag field layout
        - single_tag_st_devs (tuple[float, float, float]): The standard deviations for single tag detection
        - multi_tag_st_devs (tuple[float, float, float]): The standard deviations for multi tag detection
    """
    def __init__(self, camera_configs: Iterable[SC_CameraConfig], april_tag_field: AprilTagField, single_tag_st_devs: tuple[float, float, float], multi_tag_st_devs: tuple[float, float, float]) -> None:
        self._cameras: list[PhotonCamera] = []
        self._pose_estimators: list[PhotonPoseEstimator] = []
        self._single_tag_st_devs = single_tag_st_devs
        self._multi_tag_st_devs = multi_tag_st_devs

        april_tag_layout = AprilTagFieldLayout.loadField(april_tag_field)

        for camera_config in camera_configs:
            if camera_config.enabled:
                camera: PhotonCamera = PhotonCamera(camera_config.name)
                self._cameras.append(camera)
                self._pose_estimators.append(PhotonPoseEstimator(
                    april_tag_layout,
                    camera_config.position
                ))

    def get_camera_results(self) -> list[SC_CameraResults]:
        """
        Returns the camera results, including the estimated pose, timestamp, and standard deviation

        Returns:
            - list[SC_CameraResults]: A list of camera results
        """
        camera_results: list[SC_CameraResults] = []

        for camera, pose_estimator in zip(self._cameras, self._pose_estimators):
            for result in camera.getAllUnreadResults():
                vision_est: EstimatedRobotPose | None = pose_estimator.estimateCoprocMultiTagPose(result)
                if vision_est is None:
                    vision_est = pose_estimator.estimateLowestAmbiguityPose(result)
            
                if vision_est:
                    camera_results.append(
                        SC_CameraResults(
                            vision_est.estimatedPose.toPose2d(),
                            vision_est.timestampSeconds,
                            self._get_estimated_std_devs(
                                result, 
                                vision_est.estimatedPose.toPose2d(), 
                                pose_estimator
                            )
                        )
                    )
        
        return camera_results

    def _get_estimated_std_devs(self, result: PhotonPipelineResult, pose: Pose2d, photon_estimator: PhotonPoseEstimator) -> tuple[float, float, float]:
        """
        Returns the estimated standard deviations

        Parameters:
            - result (PhotonPipelineResult): The camera result from photon vision 
            - pose (Pose2d): The estimated pose of the robot
            - photon_estimator (PhotonPoseEstimator): The photon estimator

        Returns:
            - tuple[float, float, float]: The estimated standard deviations
        """

        est_std_dev: tuple[float, float, float] = self._single_tag_st_devs
        targets: list[PhotonTrackedTarget] = result.targets
        num_tags: int = 0
        average_distance: meters = 0.0

        for target in targets:
            tag_pose: Pose3d | None = photon_estimator.fieldTags.getTagPose(target.getFiducialId())
            if tag_pose:
                num_tags += 1
                average_distance += tag_pose.toPose2d().translation().distance(pose.translation())

        if num_tags == 0:
            return est_std_dev
        
        average_distance /= num_tags

        if num_tags > 1:
            est_std_dev = self._multi_tag_st_devs
        
        if num_tags == 1 and average_distance > meters(4):
            est_std_dev = (sys.float_info.max, sys.float_info.max, sys.float_info.max)
        else:
            scale = 1.0 + (average_distance ** 2) / 30.0
            est_std_dev = (est_std_dev[0] * scale, est_std_dev[1] * scale, est_std_dev[2] * scale)

        return est_std_dev


