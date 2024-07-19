# Motor stage UI

Offers a terminal and graphical user interface for the Mercury motor controller.
Motor stages can be arranged in a daisy chains and are controlled via [basil](https://github.com/SiLab-Bonn/basil).

## Installation

```bash
git clone https://github.com/SiLab-Bonn/basil.git
cd basil
pip install -e .
cd ..
git clone https://github.com/SiLab-Bonn/motor_stage_ui
cd motor_stage_ui
pip install -e .
```

## Usage

Check baud rate, address, USB connection and possible logic active low of the individual motor stage controller
and compare with basil/examples/lab_devices/mercury_pyserial.yaml.

Then configure stage setup in motor_stage_ui/configuration.yaml.
Set a motor stage name (x_axis), type, and step size.
With the step size given by the hardware specifics of the motor stage.

Start the motor stage GUI:
```bash
motorgui
```
or control the stage through the terminal:
```bash
motor COMMAND arguments
```
COMMAND being e.g. 'move' or 'stop' and arguments consist of a move value and the motor stage name.
Motor stage UI accepts move values in different units (mm, cm, deg, rad...) and converts them automatically. 