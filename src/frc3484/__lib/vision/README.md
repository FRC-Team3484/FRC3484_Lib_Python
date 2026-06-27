# Vision
This document shows how to use the vision utilities provided by this lib. This vision system uses PhotonVision.

> [!IMPORTANT]
> PhotonVision frequently has breaking changes. This documentation is accurate as of the 2026 season. Please update this doc accordingly if there are changes.

For vision based odometry to work, cameras must be calibrated in the PhotonVision UI. Ensure you also enable "3D" mode in the AprilTag pipeline.

First, create your camera configs and other vision constants:
```py
# constants.py
from robotpy_apriltag import AprilTagField

class VisionConstants:
    APRIL_TAG_FIELD: AprilTagField = AprilTagField.k2026RebuiltWelded
    SINGLE_TAG_STDDEV: tuple[float, float, float] = (4, 4, 8)
    MULTI_TAG_STDDEV: tuple[float, float, float] = (0.5, 0.5, 1)

    # Example camera config from the 2026 season
    CAMERA_CONFIGS: tuple[SC_CameraConfig, ...] = (
        # Forwards (turret facing)
        SC_CameraConfig(
            "Camera_1", # The name of the camera in the PhotonVision UI
            Transform3d(
                Translation3d(
                    inchesToMeters(0.75),
                    inchesToMeters(9.875),
                    inchesToMeters(20.336),
                ),  
                Rotation3d().fromDegrees(0, -30, 0)
            ),
            True
        ),
        # Backwards (intake facing)
        SC_CameraConfig(
            "Camera_2", # The name of the camera in the PhotonVision UI
            Transform3d(
                Translation3d(
                    inchesToMeters(0.25),
                    inchesToMeters(7.375),
                    inchesToMeters(20.336),
                ),  
                Rotation3d().fromDegrees(0, -30, 180)
            ),
            True
        )
    )
```

Now, create your `SC_Vision` object:
```py
# subsystem.py
from frc3484.vision import SC_Vision

self._vision: SC_Vision = SC_Vision(VisionConstants.CAMERA_CONFIGS, VisionConstants.APRIL_TAG_FIELD, VisionConstants.SINGLE_TAG_STDDEV, VisionConstants.MULTI_TAG_STDDEV)
```

Use this vision object in your drivetrain's odometry logic to get the estimated current robot position:
> [!TIP]
> It is recommended to also fall back to wheel based odometry when a camera cannot see an AprilTag. 
```py
self._odometry: SwerveDrive4PoseEstimator = SwerveDrive4PoseEstimator(
    self._kinematics,
    self._pigeon.getRotation2d(),
    self.get_module_positions(),
    Pose2d()
)

def periodic(self) -> None:
    ...

    # Wheel based odometry
    self._odometry.update(
        self._pigeon.getRotation2d(),
        self.get_module_positions()
    )

    # Camera based odometry
    if self._vision is not None:
        try:
            for result in self._vision.get_camera_results():
                new_std_devs: tuple[float, float, float] = result.standard_deviation
                self._odometry.addVisionMeasurement(
                    result.vision_measurement,
                    result.timestamp,
                    new_std_devs
                )
        except Exception as e:
            self._throw_error("Error getting vision results", e)

    ...
```