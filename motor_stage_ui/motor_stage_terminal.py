from motor_stage_ui.pi_stages_interface import PIStagesInterface as MC
import motor_stage_ui
from motor_stage_ui.pi_stages_interface import SerialInterface
from motor_stage_ui.test.utils import SerialInterfaceMock

from pathlib import Path
import os
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
            conf (str): Needs path to configuration yaml. This path is converted into a click object and passed to the individual functions.
    """
    try:
        if os.environ["TEST"]:
            path = Path(__file__).parent / "test"
            config_path = path / "test_configuration.yaml"
            test = True

    except KeyError:
        path = Path(__file__).parent
        config_path = path / "configuration.yaml"
        test = False

    conf.ensure_object(dict)
    with open(config_path, "r") as file:
        conf.obj["CONF"] = yaml.full_load(file)
    if test:
        conf.obj["MOCK"] = True
    else:
        conf.obj["MOCK"] = False


@click.command()
@click.pass_context
@click.argument("motor_name")
def init(conf, motor_name: str):
    """Initialize motor stage. Powering and resetting the motor. Set motor move speed in the PIStageInterface.py function.

    Args:
        motor_name (str): name of the motorstage
    """
    if conf.obj["MOCK"]:
        interface = SerialInterfaceMock
    else:
        interface = SerialInterface
    mc = MC(
        port=conf.obj["CONF"][motor_name]["port"],
        baud_rate=conf.obj["CONF"][motor_name]["baud_rate"],
        interface=interface,
    )
    mc.init_motor(conf.obj["CONF"][motor_name]["address"])


@click.command()
@click.pass_context
@click.argument("motor_name")
@click.option("-a", default="0", help="move value")
def move(conf, motor_name: str, a: str):
    """Moves the motor stage a relative amount, positive values for ahead, negatives for back.
    Accepts string inputs with units (4cm, -2mm...). If no unit is given, the motor moves the default unit amount.

    Args:
        motor_name (str): name of the motorstage
        a (str): Move amount
    """
    if conf.obj["MOCK"]:
        interface = SerialInterfaceMock
    else:
        interface = SerialInterface
    mc = MC(
        port=conf.obj["CONF"][motor_name]["port"],
        baud_rate=conf.obj["CONF"][motor_name]["baud_rate"],
        interface=interface,
    )
    mc.move_relative(
        conf.obj["CONF"][motor_name]["address"],
        a,
        conf.obj["CONF"][motor_name]["unit"],
        conf.obj["CONF"][motor_name]["stage_type"],
        conf.obj["CONF"][motor_name]["step_size"],
    )


@click.command()
@click.pass_context
@click.argument("motor_name")
@click.option("-a", default="0", help="move value")
def moveto(conf, motor_name: str, a: str):
    """Moves the motor stage to a absolute position.
    Accepts string inputs with units (4cm, -2mm...). If no unit is given, the motor moves to the default position unit.

    Args:
        motor_name (str): name of the motorstage
        a (str): Move to position
    """
    if conf.obj["MOCK"]:
        interface = SerialInterfaceMock
    else:
        interface = SerialInterface
    mc = MC(
        port=conf.obj["CONF"][motor_name]["port"],
        baud_rate=conf.obj["CONF"][motor_name]["baud_rate"],
        interface=interface,
    )
    mc.move_to_position(
        conf.obj["CONF"][motor_name]["address"],
        a,
        conf.obj["CONF"][motor_name]["unit"],
        conf.obj["CONF"][motor_name]["stage_type"],
        conf.obj["CONF"][motor_name]["step_size"],
    )


@click.command()
@click.pass_context
@click.argument("motor_name")
def pos(conf, motor_name: str):
    """Logs the current position of the motor stage.

    Args:
        motor_name (str): name of the motorstage
    """
    if conf.obj["MOCK"]:
        interface = SerialInterfaceMock
    else:
        interface = SerialInterface
    mc = MC(
        port=conf.obj["CONF"][motor_name]["port"],
        baud_rate=conf.obj["CONF"][motor_name]["baud_rate"],
        interface=interface,
    )
    click.echo(
        "Position of: "
        + motor_name
        + " "
        + str(
            mc.get_position(
                conf.obj["CONF"][motor_name]["address"],
                conf.obj["CONF"][motor_name]["unit"],
                conf.obj["CONF"][motor_name]["stage_type"],
                float(conf.obj["CONF"][motor_name]["step_size"]),
            )
        )
        + " "
        + conf.obj["CONF"][motor_name]["unit"]
    )


@click.command()
@click.pass_context
@click.argument("motor_name")
def stop(conf, motor_name: str):
    """Stops all movement of the motorstage.

    Args:
        motor_name (str): name of the motorstage
    """
    if conf.obj["MOCK"]:
        interface = SerialInterfaceMock
    else:
        interface = SerialInterface
    mc = MC(
        port=conf.obj["CONF"][motor_name]["port"],
        baud_rate=conf.obj["CONF"][motor_name]["baud_rate"],
        interface=interface,
    )
    mc.abort(conf.obj["CONF"][motor_name]["address"])


@click.command()
@click.pass_context
@click.argument("motor_name")
def sethome(conf, motor_name: str):
    """Sets the current position of the motorstage as absolute posiiton zero.

    Args:
        motor_name (str): name of the motorstage
    """
    if conf.obj["MOCK"]:
        interface = SerialInterfaceMock
    else:
        interface = SerialInterface
    mc = MC(
        port=conf.obj["CONF"][motor_name]["port"],
        baud_rate=conf.obj["CONF"][motor_name]["baud_rate"],
        interface=interface,
    )
    mc.set_home(conf.obj["CONF"][motor_name]["address"])


@click.command()
@click.pass_context
@click.argument("motor_name")
def gohome(conf, motor_name: str):
    """Moves the motor to the absolute position zero.

    Args:
        motor_name (str): name of the motorstage
    """
    if conf.obj["MOCK"]:
        interface = SerialInterfaceMock
    else:
        interface = SerialInterface
    mc = MC(
        port=conf.obj["CONF"][motor_name]["port"],
        baud_rate=conf.obj["CONF"][motor_name]["baud_rate"],
        interface=interface,
    )
    mc.go_home(conf.obj["CONF"][motor_name]["address"])


@click.command()
@click.pass_context
@click.argument("motor_name")
def status(conf, motor_name: str):
    """Log status of motor stage to terminal

    Args:
        motor_name (str): name of the motorstage
    """
    if conf.obj["MOCK"]:
        interface = SerialInterfaceMock
    else:
        interface = SerialInterface
    mc = MC(
        port=conf.obj["CONF"][motor_name]["port"],
        baud_rate=conf.obj["CONF"][motor_name]["baud_rate"],
        interface=interface,
    )
    click.echo(
        "Status of: "
        + motor_name
        + " "
        + str(mc.get_stat(conf.obj["CONF"][motor_name]["address"]))
    )


motor.add_command(init)
motor.add_command(move)
motor.add_command(moveto)
motor.add_command(stop)
motor.add_command(init)
motor.add_command(sethome)
motor.add_command(gohome)
motor.add_command(pos)
motor.add_command(status)
