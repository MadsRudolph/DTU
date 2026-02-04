# Regbot GUI

Python GUI for controlling the Regbot robot.

> [!info] Files Location
> The Python files are located in: `4. Semester/Linear Control Design/regbot_gui/`

## Setup

### 1. Install Python
Install Python from Microsoft Store (includes pip). Should be Python 3.x.

### 2. Install Packages
Open a terminal (cmd) and run:
```
pip install pyqt5 pyserial pyqtgraph numpy
```

### 3. Start the GUI
Navigate to the regbot_gui directory and run:
```
python regbot.py
```

> [!warning] Use PowerShell, not Git Bash
> The GUI only works from PowerShell or CMD, not from Git Bash.

## Files

The folder contains 23 Python files:

| File | Description |
|------|-------------|
| `regbot.py` | Main entry point |
| `mainwindow.py` | Main GUI window |
| `ucontrol.py` | Control interface |
| `umission.py` | Mission planning |
| `ulog.py` | Data logging |
| `ubridge.py` | Bridge communication |
| `uimu.py` | IMU sensor interface |
| `upose.py` | Pose estimation |
| `uservo.py` | Servo control |

## More Info

See the [Regbot Wiki](https://rsewiki.electro.dtu.dk/index.php?title=Regbot_GUI) for full documentation.
