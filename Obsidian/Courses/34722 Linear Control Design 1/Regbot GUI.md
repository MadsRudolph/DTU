---
course: "34722"
course-name: "Linear Control Design 1"
type: reference
tags: [LCD, reference]
---
# Regbot GUI

> [!example] Related Materials
> - Robot data analysis: [[Day 1 - MATLAB Exercise#Section 6 Robot Data Analysis]]

Python GUI for controlling the Regbot robot.

> [!info] Files Location
> The Python files are located in: [regbot_gui/](file:///C:/Users/Mads2/DTU/4.%20Semester/Linear%20Control%20Design/regbot_gui/)

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
| [regbot.py](file:///C:/Users/Mads2/DTU/4.%20Semester/Linear%20Control%20Design/regbot_gui/regbot.py) | Main entry point |
| [mainwindow.py](file:///C:/Users/Mads2/DTU/4.%20Semester/Linear%20Control%20Design/regbot_gui/mainwindow.py) | Main GUI window |
| [ucontrol.py](file:///C:/Users/Mads2/DTU/4.%20Semester/Linear%20Control%20Design/regbot_gui/ucontrol.py) | Control interface |
| [umission.py](file:///C:/Users/Mads2/DTU/4.%20Semester/Linear%20Control%20Design/regbot_gui/umission.py) | Mission planning |
| [ulog.py](file:///C:/Users/Mads2/DTU/4.%20Semester/Linear%20Control%20Design/regbot_gui/ulog.py) | Data logging |
| [ubridge.py](file:///C:/Users/Mads2/DTU/4.%20Semester/Linear%20Control%20Design/regbot_gui/ubridge.py) | Bridge communication |
| [uimu.py](file:///C:/Users/Mads2/DTU/4.%20Semester/Linear%20Control%20Design/regbot_gui/uimu.py) | IMU sensor interface |
| [upose.py](file:///C:/Users/Mads2/DTU/4.%20Semester/Linear%20Control%20Design/regbot_gui/upose.py) | Pose estimation |
| [uservo.py](file:///C:/Users/Mads2/DTU/4.%20Semester/Linear%20Control%20Design/regbot_gui/uservo.py) | Servo control |

## More Info

See the [Regbot Wiki](https://rsewiki.electro.dtu.dk/index.php?title=Regbot_GUI) for full documentation.

---

> [!nav]
> &nbsp;
>
> [[34722 Linear Control Design 1|34722 Home]]
>
> &nbsp;
