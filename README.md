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