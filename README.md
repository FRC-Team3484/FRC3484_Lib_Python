# FRC3484_Lib

This repository holds common code for 3484 in Python

## Included Features
- **Controls** - Abstracts the hardware controller inputs, to allow for any controller input to appear as any other type. This implements a more convenient interface for interacting with OI
- **LEDs** - Common LED code for robots
- **Motion** - Motor template classes, which allows for creating motors in subsystems without any of the repeated code for setup, PID, and feed forward.
- **Pathfinding** - Code for handling pathfinding with Pathplanner, and for finely aligning to locations on the fields
- **Pose Manipulation** - Helper functions for handling AprilTag poses and applying offsets to them
- **Vision** - Code for getting the current pose of the robot based on visible AprilTags

## Installing
Clone this repository:
```bash
git clone https://github.com/FRC-Team3484/FRC3484_Lib_Python
cd FRC3484_Lib_Python
```
Or, use `Git: Clone` in the VSCode command palate (`Ctrl+Shift+P`)

Create a new virtual environment and activate it:
```bash
python -m venv .venv
source ./.venv/bin/activate
```
Or, with the Python VSCode extension, click the Python version number in the bottom right, and select `Create Virtual Enviroment`

Install the dependencies:
```bash
pip install uv
uv sync
```