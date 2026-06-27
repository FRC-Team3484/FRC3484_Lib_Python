# Pose Manipulation
This document goes over each pose manipulation function provided by this lib.

- `get_april_tag_pose` - Given an `april_tag_id` and an `AprilTagFieldLayout`, return the pose of that AprilTag.
- `get_april_tag_poses` - Given several `april_tag_ids` and a `AprilTagFieldLayout`, return a list of AprilTag poses.
- `apply_offset_to_pose` - Given a `pose` and `offset`, return that pose with that offset applied.
- `apply_offsets_to_poses` - Given a list of `poses` and a list of `offsets`, return a list of each pose with each offset applied. If two poses and two offsets are provided, four poses are returned.
- `get_nearest_pose` - Given `current_position` and a list of `poses`, return the pose that is the closest to `current_position`.