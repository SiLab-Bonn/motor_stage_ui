# Motor stage UI
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Offers both a terminal and graphical user interface for the Mercury motor controller.
Motor stages can be arranged in daisy chains.

## Installation

```bash
git clone https://github.com/SiLab-Bonn/motor_stage_ui
cd motor_stage_ui
pip install -e .
```

## Usage

Configure your specific stage setup in ```motor_stage_ui/configuration.yaml```.
Check the baud rate, address, USB connection, and any potential logic active low settings for the individual motor stage controller.
Set a motor stage name (e.g., ```x_axis```), type, and step size according to the hardware specifications of the motor stage.

Start the motor stage GUI:
```bash
motorgui
```
or control the stage through the terminal:
```bash
motor COMMAND arguments
```
The ```COMMAND``` can be ```move``` or ```stop```, and the arguments consist of a move value and the motor stage name.
The motor stage UI accepts move values in various units (mm, cm, deg, rad, etc.) and converts them automatically.

The motor stage velocity is set during the initialization step. To avoid unwanted behavior (especially if the default motor speed is too slow), ensure to initialize the motor stage even when using the terminal.

```bash
motor init MOTORNAME
```

### Configuration

| Configuration | Description | Type |
|-----------|-------------|------|
| `stage_type` | Type of the motor stage (translation or rotation) | String |
| `address` | Address of the specific motor controller (set on the motor controller) | Integer |
| `step_size` | Step size of the motor stage (given in um for translation and deg for rotation stages) | Integer |
| `unit` | Default unit of the motor stage | String |
| `port` | Serial port to connect to | String |
| `baud_rate` | Baud rate of the motor controller (set on the motor controller) | String |

### Commands

| Terminal Command | GUI Command |  Description | First Argument | Second Argument |
|---------|-------------|-----------|-----------|-----------|
| `init` | `Init.` | Initialize motor stage. Powering and resetting the motor. Set motor move speed in the PIStageInterface.py function.| motor_name (str): name of the motorstage | - |
| `move` | `Input rel.` | Moves the motor stage a relative amount, positive values for ahead, negatives for back. Accepts string inputs with units (4cm, -2mm...). If no unit is given, the motor moves the default unit amount. | motor_name (str): name of the motorstage | a (str): Move amount |
| `moveto` | `input abs.` | Moves the motor stage to a absolut position. Accepts string inputs with units (4cm, -2mm...). If no unit is given, the motor moves to the default position unit. | motor_name (str): name of the motorstage |a (str): Move to position |
| `pos` | - | Logs the current position of the motor stage.| motor_name (str): name of the motorstage | -|
| `stop` | `Stop` | Immediately stops all movement of the stage | motor_name (str): name of the motorstage | - |
| `sethome` | `Set Zero` | Sets the current position of the stage as new origin | motor_name (str): name of the motorstage | - |
| `gohome` | `MV. Zero` | Goes to origin of the stage | motor_name (str): name of the motorstage | - |
