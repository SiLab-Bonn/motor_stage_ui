from pathlib import Path
import yaml
import pytest
from motor_stage_ui.motor_stage_gui import MainWindow
from motor_stage_ui.test.utils import SerialInterfaceMock
from PyQt5 import QtCore
import logging

FILEPATH = Path(__file__).parent
CONFIG_FILE = FILEPATH / "test_configuration.yaml"

INTERFACE = SerialInterfaceMock
with open(CONFIG_FILE) as yaml_file:
    TESTCONFIG = yaml.safe_load(yaml_file)


@pytest.fixture
def app(qtbot):
    motor_gui = MainWindow(CONFIG_FILE, interface=INTERFACE)
    return motor_gui


def test_init_clicked(app):
    ADDRESS = TESTCONFIG["x_axis"]["address"]
    app.init_clicked(address=ADDRESS, index=0)
    assert app.motor[0].serial_interface._serial_commands[-3:] == [
        b"\x010MN\r",
        b"\x010RT\r",
        b"\x010SV200000\r",
    ]

    ADDRESS = TESTCONFIG["rot"]["address"]
    app.init_clicked(address=ADDRESS, index=1)
    assert app.motor[1].serial_interface._serial_commands[-3:] == [
        b"\x012MN\r",
        b"\x012RT\r",
        b"\x012SV200000\r",
    ]


def test_move_back_clicked(app):
    ADDRESS = TESTCONFIG["x_axis"]["address"]
    UNIT = TESTCONFIG["x_axis"]["unit"]
    STEPSIZE = TESTCONFIG["x_axis"]["step_size"]
    STAGE = TESTCONFIG["x_axis"]["stage_type"]
    app.move_back_clicked(
        address=ADDRESS, unit=UNIT, stage=STAGE, step_size=STEPSIZE, index=0
    )
    assert app.motor[0].serial_interface._serial_commands[-1] == b"\x010MR-55555\r"

    ADDRESS = TESTCONFIG["rot"]["address"]
    UNIT = TESTCONFIG["rot"]["unit"]
    STEPSIZE = float(TESTCONFIG["rot"]["step_size"])
    STAGE = TESTCONFIG["rot"]["stage_type"]
    app.move_back_clicked(
        address=ADDRESS, unit=UNIT, stage=STAGE, step_size=STEPSIZE, index=1
    )
    assert app.motor[1].serial_interface._serial_commands[-1] == b"\x012MR-29411\r"


def test_move_ahead_clicked(app):
    ADDRESS = TESTCONFIG["x_axis"]["address"]
    UNIT = TESTCONFIG["x_axis"]["unit"]
    STEPSIZE = TESTCONFIG["x_axis"]["step_size"]
    STAGE = TESTCONFIG["x_axis"]["stage_type"]
    app.move_ahead_clicked(
        address=ADDRESS, unit=UNIT, stage=STAGE, step_size=STEPSIZE, index=0
    )
    assert app.motor[0].serial_interface._serial_commands[-1] == b"\x010MR55555\r"

    ADDRESS = TESTCONFIG["rot"]["address"]
    UNIT = TESTCONFIG["rot"]["unit"]
    STEPSIZE = float(TESTCONFIG["rot"]["step_size"])
    STAGE = TESTCONFIG["rot"]["stage_type"]
    app.move_ahead_clicked(
        address=ADDRESS, unit=UNIT, stage=STAGE, step_size=STEPSIZE, index=1
    )
    assert app.motor[1].serial_interface._serial_commands[-1] == b"\x012MR29411\r"


def test_abort_clicked(app):
    ADDRESS = TESTCONFIG["x_axis"]["address"]
    app.abort_clicked(address=ADDRESS, index=0)
    assert app.motor[0].serial_interface._serial_commands[-1] == b"\x010AB\r"

    ADDRESS = TESTCONFIG["rot"]["address"]
    app.abort_clicked(address=ADDRESS, index=1)
    assert app.motor[1].serial_interface._serial_commands[-1] == b"\x012AB\r"


def test_set_home_clicked(app):
    ADDRESS = TESTCONFIG["x_axis"]["address"]
    app.set_home_clicked(address=ADDRESS, index=0)
    assert app.motor[0].serial_interface._serial_commands[-1] == b"\x010DH\r"

    ADDRESS = TESTCONFIG["rot"]["address"]
    app.set_home_clicked(address=ADDRESS, index=1)
    assert app.motor[1].serial_interface._serial_commands[-1] == b"\x012DH\r"


def test_go_home_clicked(app):
    ADDRESS = TESTCONFIG["x_axis"]["address"]
    app.go_home_clicked(address=ADDRESS, index=0)
    assert app.motor[0].serial_interface._serial_commands[-1] == b"\x010GH\r"

    ADDRESS = TESTCONFIG["rot"]["address"]
    app.go_home_clicked(address=ADDRESS, index=1)
    assert app.motor[1].serial_interface._serial_commands[-1] == b"\x012GH\r"


def test_set_position_abs_clicked(app):
    ADDRESS = TESTCONFIG["x_axis"]["address"]
    UNIT = TESTCONFIG["x_axis"]["unit"]
    STEPSIZE = TESTCONFIG["x_axis"]["step_size"]
    STAGE = TESTCONFIG["x_axis"]["stage_type"]
    app.set_position_abs_clicked(
        address=ADDRESS,
        textbox="2cm",
        unit=UNIT,
        stage=STAGE,
        step_size=STEPSIZE,
        index=0,
    )
    assert app.motor[0].serial_interface._serial_commands[-1] == b"\x010MA1111111\r"

    ADDRESS = TESTCONFIG["rot"]["address"]
    UNIT = TESTCONFIG["rot"]["unit"]
    STEPSIZE = float(TESTCONFIG["rot"]["step_size"])
    STAGE = TESTCONFIG["rot"]["stage_type"]
    app.set_position_abs_clicked(
        address=ADDRESS,
        textbox="1deg",
        unit=UNIT,
        stage=STAGE,
        step_size=STEPSIZE,
        index=1,
    )
    assert app.motor[1].serial_interface._serial_commands[-1] == b"\x012MA29411\r"


def test_set_position_rel_clicked(app):
    ADDRESS = TESTCONFIG["x_axis"]["address"]
    UNIT = TESTCONFIG["x_axis"]["unit"]
    STEPSIZE = TESTCONFIG["x_axis"]["step_size"]
    STAGE = TESTCONFIG["x_axis"]["stage_type"]
    app.set_position_rel_clicked(
        address=ADDRESS,
        textbox="2cm",
        unit=UNIT,
        stage=STAGE,
        step_size=STEPSIZE,
        index=0,
    )
    assert app.motor[0].serial_interface._serial_commands[-1] == b"\x010MR1111111\r"

    ADDRESS = TESTCONFIG["rot"]["address"]
    UNIT = TESTCONFIG["rot"]["unit"]
    STEPSIZE = float(TESTCONFIG["rot"]["step_size"])
    STAGE = TESTCONFIG["rot"]["stage_type"]
    app.set_position_rel_clicked(
        address=ADDRESS,
        textbox="1.5deg",
        unit=UNIT,
        stage=STAGE,
        step_size=STEPSIZE,
        index=1,
    )
    assert app.motor[1].serial_interface._serial_commands[-1] == b"\x012MR44117\r"


def test_get_position_clicked(app):
    ADDRESS = TESTCONFIG["x_axis"]["address"]
    UNIT = TESTCONFIG["x_axis"]["unit"]
    STEPSIZE = TESTCONFIG["x_axis"]["step_size"]
    STAGE = TESTCONFIG["x_axis"]["stage_type"]
    app.get_position_clicked(
        address=ADDRESS, unit=UNIT, stage=STAGE, step_size=STEPSIZE, index=0
    )
    assert app.motor[0].serial_interface._serial_commands[-1] == b"\x010TP\r"

    ADDRESS = TESTCONFIG["rot"]["address"]
    UNIT = TESTCONFIG["rot"]["unit"]
    STEPSIZE = float(TESTCONFIG["rot"]["step_size"])
    STAGE = TESTCONFIG["rot"]["stage_type"]
    app.get_position_clicked(
        address=ADDRESS, unit=UNIT, stage=STAGE, step_size=STEPSIZE, index=1
    )
    assert app.motor[1].serial_interface._serial_commands[-1] == b"\x012TP\r"


if __name__ == "__main__":
    pytest.main()
