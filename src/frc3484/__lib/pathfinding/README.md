# Pathfinding

This document goes over this lib's provided features for robot pathfinding. This is not the same as following paths through PathPlanner, instead these functions create commands for driving the robot automatically to poses, while avoiding obstacles.

> [!IMPORTANT]
> The Python implementation of these features has not yet been fully tested in a competition robot. For now, this document only lists a brief description of each function and when to use it. Once these have been tested, add better example code here.

First, create a `SC_Pathfinding` object. It takes the `drivetrain_subsystem`, a function that supplies the robot's current pose, a function to output a `ChassisSpeeds` object to the drivetrain, and a `PathFollowingController` to use for final alignment.

This object provides the following functions:
- `get_final_alignment_command` - Returns a command to align the robot to a target pose.
- `get_near_pose_command` - Returns a command that does nothing and waits until the robot is within a distance, then exits. This is intended to be used in a race group with a pathing command, so that the robot stops pathing once it is close enough to the end position.
- `get_pathfollow_command` - Returns a command that drives from a start pose to a target pose, without any obstacle avoidance. Optionally, intermediate points for the path can be provided.
- `get_pathfind_command` - Returns a command that drives to a target pose, avoiding obstacles.
- `pathfind_to_pose` - Returns a command that drives to the given target pose, while avoiding obstacles. It uses the `get_near_pose_command` to end the pathfinding command early, then uses the `FinalAlignmentCommand` to do the last few inches.