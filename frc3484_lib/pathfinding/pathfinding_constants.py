from dataclasses import dataclass

from wpimath.units import inches, degrees

from pathplannerlib.path import PathConstraints

@dataclass(frozen=True)
class PathfindingCommandConstants:
    PATH_CONSTRAINTS: PathConstraints = PathConstraints(
        maxVelocityMps=3.0, 
        maxAccelerationMpsSq=4.0,
        maxAngularVelocityRps=540.0, 
        maxAngularAccelerationRpsSq=720.0
    )

@dataclass(frozen=True)
class FinalAlignmentCommandConstants:
    FINAL_ALIGN_EXIT: int = 1000000
    FINAL_POSE_TOLERANCE: inches = 0.3
    FINAL_ROTATION_TOLERANCE: degrees = 1