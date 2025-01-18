from pathlib import Path
import pytest
import yaml
from motor_stage_ui.pi_stages_interface import PIStagesInterface
from motor_stage_ui.test.utils import SerialInterfaceMock


FILEPATH = Path(__file__).parent
CONFIG_FILE = FILEPATH / "test_configuration.yaml"

with open(CONFIG_FILE) as yaml_file:
    TESTCONFIG = yaml.safe_load(yaml_file)


INTERFACE = SerialInterfaceMock

PISTAGES = PIStagesInterface(
    port=TESTCONFIG["x_axis"]["port"],
    baud_rate=TESTCONFIG["x_axis"]["baud_rate"],
    interface=INTERFACE,
)


def test_init_motor():
    ADDRESS = TESTCONFIG["x_axis"]["address"]
    PISTAGES.init_motor(address=ADDRESS)
    assert PISTAGES.serial_interface._serial_commands[-3:] == [
        b"\x010MN\r",
        b"\x010RT\r",
        b"\x010SV200000\r",
    ]

    ADDRESS = TESTCONFIG["rot"]["address"]
    PISTAGES.init_motor(address=ADDRESS)
    assert PISTAGES.serial_interface._serial_commands[-3:] == [
        b"\x012MN\r",
        b"\x012RT\r",
        b"\x012SV200000\r",
    ]


def test_motor_off():
    ADDRESS = TESTCONFIG["x_axis"]["address"]
    PISTAGES.motor_off(address=ADDRESS)
    assert PISTAGES.serial_interface._serial_commands[-1] == b"\x010MF\r"

    ADDRESS = TESTCONFIG["rot"]["address"]
    PISTAGES.motor_off(address=ADDRESS)
    assert PISTAGES.serial_interface._serial_commands[-1] == b"\x012MF\r"


def test_find_edge():
    ADDRESS = TESTCONFIG["x_axis"]["address"]
    UNIT = TESTCONFIG["x_axis"]["unit"]
    STEPSIZE = TESTCONFIG["x_axis"]["step_size"]
    STAGE = TESTCONFIG["x_axis"]["stage_type"]

    PISTAGES.find_edge(address=ADDRESS, unit=UNIT, stage=STAGE, step_size=STEPSIZE)
    assert PISTAGES.serial_interface._serial_commands[-1] == b"\x010TP\r"

    ADDRESS = TESTCONFIG["rot"]["address"]
    UNIT = TESTCONFIG["rot"]["unit"]
    STEPSIZE = float(TESTCONFIG["rot"]["step_size"])
    STAGE = TESTCONFIG["rot"]["stage_type"]

    PISTAGES.find_edge(address=ADDRESS, unit=UNIT, stage=STAGE, step_size=STEPSIZE)
    assert PISTAGES.serial_interface._serial_commands[-1] == b"\x012TP\r"


def test_set_home() -> None:
    ADDRESS = TESTCONFIG["x_axis"]["address"]
    PISTAGES.set_home(address=ADDRESS)
    assert PISTAGES.serial_interface._serial_commands[-1] == b"\x010DH\r"

    ADDRESS = TESTCONFIG["rot"]["address"]
    PISTAGES.set_home(address=ADDRESS)
    assert PISTAGES.serial_interface._serial_commands[-1] == b"\x012DH\r"


def test_go_home() -> None:
    ADDRESS = TESTCONFIG["x_axis"]["address"]
    PISTAGES.go_home(address=ADDRESS)
    assert PISTAGES.serial_interface._serial_commands[-1] == b"\x010GH\r"

    ADDRESS = TESTCONFIG["rot"]["address"]
    PISTAGES.go_home(address=ADDRESS)
    assert PISTAGES.serial_interface._serial_commands[-1] == b"\x012GH\r"


def test_abort():
    ADDRESS = TESTCONFIG["x_axis"]["address"]
    PISTAGES.abort(address=ADDRESS)
    assert PISTAGES.serial_interface._serial_commands[-1] == b"\x010AB\r"

    ADDRESS = TESTCONFIG["rot"]["address"]
    PISTAGES.abort(address=ADDRESS)
    assert PISTAGES.serial_interface._serial_commands[-1] == b"\x012AB\r"


def test_move_to_position():
    ADDRESS = TESTCONFIG["x_axis"]["address"]
    UNIT = TESTCONFIG["x_axis"]["unit"]
    STEPSIZE = TESTCONFIG["x_axis"]["step_size"]
    STAGE = TESTCONFIG["x_axis"]["stage_type"]
    PISTAGES.move_to_position(
        address=ADDRESS, amount="1mm", unit=UNIT, stage=STAGE, step_size=STEPSIZE
    )
    assert PISTAGES.serial_interface._serial_commands[-1] == b"\x010MA55555\r"

    ADDRESS = TESTCONFIG["rot"]["address"]
    UNIT = TESTCONFIG["rot"]["unit"]
    STEPSIZE = float(TESTCONFIG["rot"]["step_size"])
    STAGE = TESTCONFIG["rot"]["stage_type"]
    PISTAGES.move_to_position(
        address=ADDRESS, amount="1deg", unit=UNIT, stage=STAGE, step_size=STEPSIZE
    )
    assert PISTAGES.serial_interface._serial_commands[-1] == b"\x012MA29411\r"


def test_move_relative():
    ADDRESS = TESTCONFIG["x_axis"]["address"]
    UNIT = TESTCONFIG["x_axis"]["unit"]
    STEPSIZE = TESTCONFIG["x_axis"]["step_size"]
    STAGE = TESTCONFIG["x_axis"]["stage_type"]
    PISTAGES.move_relative(
        address=ADDRESS, amount="-1cm", unit=UNIT, stage=STAGE, step_size=STEPSIZE
    )
    assert PISTAGES.serial_interface._serial_commands[-1] == b"\x010MR-555555\r"

    ADDRESS = TESTCONFIG["rot"]["address"]
    UNIT = TESTCONFIG["rot"]["unit"]
    STEPSIZE = float(TESTCONFIG["rot"]["step_size"])
    STAGE = TESTCONFIG["rot"]["stage_type"]
    PISTAGES.move_relative(
        address=ADDRESS, amount="-1rad", unit=UNIT, stage=STAGE, step_size=STEPSIZE
    )
    assert PISTAGES.serial_interface._serial_commands[-1] == b"\x012MR-1685169\r"


def test_get_position():
    ADDRESS = TESTCONFIG["x_axis"]["address"]
    UNIT = TESTCONFIG["x_axis"]["unit"]
    STEPSIZE = TESTCONFIG["x_axis"]["step_size"]
    STAGE = TESTCONFIG["x_axis"]["stage_type"]

    assert (
        PISTAGES.get_position(
            address=ADDRESS, unit=UNIT, stage=STAGE, step_size=STEPSIZE
        )
        == "0.000"
    )

    ADDRESS = TESTCONFIG["rot"]["address"]
    UNIT = TESTCONFIG["rot"]["unit"]
    STEPSIZE = float(TESTCONFIG["rot"]["step_size"])
    STAGE = TESTCONFIG["rot"]["stage_type"]

    assert (
        PISTAGES.get_position(
            address=ADDRESS, unit=UNIT, stage=STAGE, step_size=STEPSIZE
        )
        == "0.000"
    )


def test_get_stat():
    ADDRESS = TESTCONFIG["x_axis"]["address"]
    PISTAGES.get_stat(address=ADDRESS)
    assert PISTAGES.serial_interface._serial_commands[-1] == b"\x010TS\r"

    ADDRESS = TESTCONFIG["rot"]["address"]
    PISTAGES.get_stat(address=ADDRESS)
    assert PISTAGES.serial_interface._serial_commands[-1] == b"\x012TS\r"


if __name__ == "__main__":
    pytest.main()
