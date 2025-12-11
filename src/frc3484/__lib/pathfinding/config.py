from dataclasses import dataclass

from wpimath.units import inches, degrees, seconds

from pathplannerlib.path import PathConstraints

@dataclass(frozen=True)
class PathfindingConfig:
    FINAL_ALIGNMENT_DISTANCE: inches = 6.0
    PATH_CONSTRAINTS: PathConstraints = PathConstraints(
        maxVelocityMps=3.0, 
        maxAccelerationMpsSq=4.0,
        maxAngularVelocityRps=540.0, 
        maxAngularAccelerationRpsSq=720.0
    )

@dataclass(frozen=True)
class FinalAlignmentConfig:
    TIMEOUT: seconds = 3.0
    POSITION_TOLERANCE: inches = 0.3
    ROTATION_TOLERANCE: degrees = 1