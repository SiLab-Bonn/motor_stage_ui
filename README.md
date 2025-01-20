# Motor stage UI
[![pre-commit](https://github.com/SiLab-Bonn/motor_stage_ui/actions/workflows/pre_commit.yml/badge.svg)](https://github.com/SiLab-Bonn/motor_stage_ui/actions/workflows/pre_commit.yml)
[![Tests](https://github.com/SiLab-Bonn/motor_stage_ui/actions/workflows/tests.yml/badge.svg)](https://github.com/SiLab-Bonn/motor_stage_ui/actions/workflows/tests.yml)

Offers both a terminal and graphical user interface for the [C-863 Mercury controller](https://www.le.infn.it/~chiodini/allow_listing/pi/Manuals/C-863_UserManual_MS205E200.pdf) (Check also the [commands](https://twiki.cern.ch/twiki/bin/viewfile/ILCBDSColl/Phase2Preparations?rev=1;filename=MercuryNativeCommands_MS176E101.pdf)).
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
The step size of a specific stage is given in um for translation stages and deg for rotation stages and can be obtained from the 'Design resolution' in e.g. [PI precision position and motion control](https://www.pi-usa.us/fileadmin/user_upload/physik_instrumente/files/CAT/PI-CAT132E-Precision-Positioning-and-Motion-Control-Web.pdf).

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
| `moveto` | `input abs.` | Moves the motor stage to an absolute position. Accepts string inputs with units (4cm, -2mm...). If no unit is given, the motor moves to the default position unit. | motor_name (str): name of the motorstage |a (str): Move to position |
| `pos` | - | Logs the current position of the motor stage.| motor_name (str): name of the motorstage | -|
| `stop` | `Stop` | Immediately stops all movement of the stage | motor_name (str): name of the motorstage | - |
| `sethome` | `Set Zero` | Sets the current position of the stage as new origin | motor_name (str): name of the motorstage | - |
| `gohome` | `MV. Zero` | Goes to origin of the stage | motor_name (str): name of the motorstage | - |
| `status` | - | Returns the status of the motor controller | motor_name (str): name of the motorstage | - |

## Tests

General UI tests, utilizing a motor controller mock, are performed when setting the environmental variable `TEST` e.g.:

```bash
TEST=True motor init x_axis
```

```bash
TEST=True motorgui
```
[Pytest](https://docs.pytest.org/en/stable/) is used to test the software.
Here, a serial interface mock is used.
Install test dependencies with:

```bash
pip install -e .[test]
```
and test the software with logging:

```bash
pytest -sv
```
