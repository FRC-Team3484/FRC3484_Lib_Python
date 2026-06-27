# FRC3484_Lib

This repository holds common code for 3484 in Python

## Included Features
- [**Controls**](/src/frc3484/__lib/controls/README.md) - Abstracts the hardware controller inputs, to allow for any controller input to appear as any other type. This implements a more convenient interface for interacting with OI
- **LEDs** - Common LED code for robots
- [**Motion**](/src/frc3484/__lib/motion/README.md) - Motor template classes, which allows for creating motors in subsystems without any of the repeated code for setup, PID, and feed forward.
- [**Pathfinding**](/src/frc3484/__lib/pathfinding/README.md) - Code for handling pathfinding with Pathplanner, and for finely aligning to locations on the fields
- [**Pose Manipulation**](/src/frc3484/__lib/pose_manipulation/README.md) - Helper functions for handling AprilTag poses and applying offsets to them
- [**Vision**](/src/frc3484/__lib/vision/README.md) - Code for getting the current pose of the robot based on visible AprilTags

## Installing
### Pip
Open your robot project, and create a virtual environment:
```bash
cd RobotCode
python -m venv .venv
source ./.venv/bin/activate # This may vary depending on your OS
```

Install the library:
```bash
pip install git+https://github.com/FRC-Team3484/FRC3484_Lib_Python
```

### Pyproject
Add the following to your `pyproject.toml`:
```toml
requires = [
    "frc3484 @ git+https://github.com/FRC-Team3484/FRC3484_Lib_Python.git@main"
]
```

Then, update the `robotpy` cache:
```bash
robotpy sync
```

## Updating
### Locally
If installed with pip, you may have to forcefully reinstall the library to get the new changes:
```bash
pip install git+https://github.com/FRC-Team3484/FRC3484_Lib_Python --no-cache-dur
```

### On Robot
When deploying this lib with robot code, you may need to forcefully reinstall all of the packages to get library changes to apply:
```bash
robotpy deploy --force-install
```

## Installing for Development
Clone this repository:
```bash
git clone https://github.com/FRC-Team3484/FRC3484_Lib_Python
cd FRC3484_Lib_Python
```
Or, use `Git: Clone` in the VSCode command palate (`Ctrl+Shift+P`)

Create a new virtual environment and activate it:
```bash
python -m venv .venv
source ./.venv/bin/activate # This may vary depending on your OS
```
Or, with the Python VSCode extension, click the Python version number in the bottom right, and select `Create Virtual Enviroment`

Install the dependencies:
```bash
pip install uv
uv sync
```