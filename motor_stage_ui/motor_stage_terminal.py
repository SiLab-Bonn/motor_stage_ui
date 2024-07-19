from motor_stage_ui.motor_controller import MotorController as MC 

import click
import yaml

"""

Terminal control UI.      

"""

@click.group()
@click.pass_context
def motor(conf):
    """Terminal interface for control of the mercury motor controller.
    write e.g. motor move -a amount NAME to move stage NAME amount units.
    Amount can be in different units (3mm, 2cm..). If something does not work check first the configuration file 
    (also in basil).

        Args:
            conf (str): Needs path to configuration yaml. This path is convertet into a click object and passed to the individual functions.
    """
    conf.ensure_object(dict)
    config_path = 'motor_stage_ui/configuration.yaml'
    with open(config_path, "r") as file:
        conf.obj['CONF'] = yaml.full_load(file)

@click.command()
@click.pass_context
@click.argument('motorname')
def init(conf, motorname):
    """Initialize motor stage. Powering and resetting the motor. Set motor move speed in the motor_controller.py function.

    Args:
        motorname (str): name of the motorstage
    """
    MC().init_motor(conf.obj['CONF'][motorname]['address'])

@click.command()
@click.pass_context
@click.argument('motorname')
@click.option('-a', default='0', help='move value')
def move(conf, motorname, a):
    """Moves the motor stage a relative amount, positive values for ahead, negatives for back.
    Accepts string inputs with units (4cm, -2mm...). If no unit is given, the motor moves the default unit amount.

    Args:
        motorname (str): name of the motorstage
        a (str): Move amount
    """
    MC().move_relative(conf.obj['CONF'][motorname]['address'], a, conf.obj['CONF'][motorname]['unit'], 
                          conf.obj['CONF'][motorname]['stage'], conf.obj['CONF'][motorname]['step_size'])

@click.command()
@click.pass_context
@click.argument('motorname')
@click.option('-a', default='0', help='move value')
def moveto(conf, motorname, a):
    """Moves the motor stage to a absolut position.
    Accepts string inputs with units (4cm, -2mm...). If no unit is given, the motor moves to the default position unit.

    Args:
        motorname (str): name of the motorstage
        a (str): Move to position
    """
    MC().move_to_position(conf.obj['CONF'][motorname]['address'], a, conf.obj['CONF'][motorname]['unit'], 
                          conf.obj['CONF'][motorname]['stage'], conf.obj['CONF'][motorname]['step_size'])

@click.command()
@click.pass_context
@click.argument('motorname')
def pos(conf, motorname):  
    """Logs the current position of the motor stage.

    Args:
        motorname (str): name of the motorstage
    """
    click.echo("Position of: " + motorname + ' ' + str(MC().get_position(conf.obj['CONF'][motorname]['address'], conf.obj['CONF'][motorname]['unit'], 
                          conf.obj['CONF'][motorname]['stage'], conf.obj['CONF'][motorname]['step_size'])) + ' ' + conf.obj['CONF'][motorname]['unit'])

@click.command()
@click.pass_context
@click.argument('motorname')
def stop(conf, motorname):
    """Stops all movement of the motorstage.

    Args:
        motorname (str): name of the motorstage
    """
    MC().abort(conf.obj['CONF'][motorname]['address'])

@click.command()
@click.pass_context
@click.argument('motorname')
def sethome(conf, motorname):
    """Sets the current position of the motorstage as absolute posiiton zero.

    Args:
        motorname (str): name of the motorstage
    """
    MC().set_home(conf.obj['CONF'][motorname]['address'])

@click.command()
@click.pass_context
@click.argument('motorname')
def gohome(conf, motorname):
    """Moves the motor to the absolute position zero.

    Args:
        motorname (str): name of the motorstage
    """
    MC().go_home(conf.obj['CONF'][motorname]['address'])

motor.add_command(init)
motor.add_command(move)
motor.add_command(moveto)
motor.add_command(stop)
motor.add_command(init)
motor.add_command(sethome)
motor.add_command(gohome)
motor.add_command(pos)