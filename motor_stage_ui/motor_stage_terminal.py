from motor_stage_ui.motor_controller import MotorController as MC 

import click
import yaml

@click.group()
@click.pass_context
def motor(conf):
    """Terminal interface for control of the mercury motor controller.
    write e.q. motor move -a amount NAME to move stage NAME amount units.
    Amount can be in different units (3mm, 2cm..). If something does not work check first the configuration file 
    (also in basil).
    """
    conf.ensure_object(dict)
    config_path = 'motor_stage_ui/configuration.yaml'
    with open(config_path, "r") as file:
        conf.obj['CONF'] = yaml.full_load(file)

@click.command()
@click.pass_context
@click.argument('motorname')
def init(conf, motorname):
    MC().init_motor(conf.obj['CONF'][motorname]['address'])

@click.command()
@click.pass_context
@click.argument('motorname')
@click.option('-a', default='0', help='move value')
def move(conf, motorname, a):
    MC().move_relative(conf.obj['CONF'][motorname]['address'], a, conf.obj['CONF'][motorname]['unit'], 
                          conf.obj['CONF'][motorname]['stage'], conf.obj['CONF'][motorname]['step_size'])

@click.command()
@click.pass_context
@click.argument('motorname')
@click.option('-a', default='0', help='move value')
def moveto(conf, motorname, a):
    MC().move_to_position(conf.obj['CONF'][motorname]['address'], a, conf.obj['CONF'][motorname]['unit'], 
                          conf.obj['CONF'][motorname]['stage'], conf.obj['CONF'][motorname]['step_size'])

@click.command()
@click.pass_context
@click.argument('motorname')
def pos(conf, motorname):
    click.echo("Position of: " + motorname + ' ' + str(MC().get_position(conf.obj['CONF'][motorname]['address'], conf.obj['CONF'][motorname]['unit'], 
                          conf.obj['CONF'][motorname]['stage'], conf.obj['CONF'][motorname]['step_size'])) + ' ' + conf.obj['CONF'][motorname]['unit'])

@click.command()
@click.pass_context
@click.argument('motorname')
def stop(conf, motorname):
    MC().abort(conf.obj['CONF'][motorname]['address'])

@click.command()
@click.pass_context
@click.argument('motorname')
def sethome(conf, motorname):
    MC().set_home(conf.obj['CONF'][motorname]['address'])

@click.command()
@click.pass_context
@click.argument('motorname')
def gohome(conf, motorname):
    MC().go_home(conf.obj['CONF'][motorname]['address'])

motor.add_command(init)
motor.add_command(move)
motor.add_command(moveto)
motor.add_command(stop)
motor.add_command(init)
motor.add_command(sethome)
motor.add_command(gohome)
motor.add_command(pos)