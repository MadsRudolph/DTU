# Regbot GUI

Python GUI for controlling the Regbot robot.

## Install Python

### Windows
Install Python from Microsoft Store (includes pip). Should be Python 3.x.

### Mac
Install Python 3.x (may be installed by default).

### Linux
```bash
sudo apt install python3
sudo apt install pip
```

## Install Python Packages

### Windows
Open a terminal (cmd) and run:
```bash
pip install pyqt5
pip install pyserial
pip install pyqtgraph
pip install numpy
```

### Mac
Same packages as Windows.

### Linux
Either use pip:
```bash
pip install pyqt5
pip install pyqtgraph
pip install pyserial
pip install numpy
```

Or install with apt:
```bash
sudo apt install python3-pyqt5
sudo apt install python3-serial
sudo apt install python3-pyqtgraph
```

## Start the Regbot GUI

Navigate to this directory and run:
```bash
python regbot.py
```

Or on Linux/Mac:
```bash
python3 regbot.py
```

## Files

This folder contains 23 Python files for the GUI:
- `regbot.py` - Main entry point
- `mainwindow.py` - Main GUI window
- `ucontrol.py` - Control interface
- `umission.py` - Mission planning
- `ulog.py` - Data logging
- And more...

## More Info

See the [Regbot Wiki](https://rsewiki.elektro.dtu.dk/index.php/Regbot) for full documentation.
