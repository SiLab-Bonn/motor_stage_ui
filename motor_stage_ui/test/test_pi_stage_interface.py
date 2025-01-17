from pathlib import Path
import os
import pytest
import yaml
from motor_stage_ui.pi_stages_interface import PIStagesInterface
from motor_stage_ui.pi_stages_interface import SerialInterface
from motor_stage_ui.test.utils import SerialInterfaceMock


FILEPATH = Path(__file__).parent
CONFIG_FILE = FILEPATH / "test_configuration.yaml"

with open(CONFIG_FILE) as yaml_file:
    TESTCONFIG = yaml.safe_load(yaml_file)
ADDRESS = TESTCONFIG["x_axis"]["address"]
UNIT = TESTCONFIG["x_axis"]["unit"]
STEPSIZE = TESTCONFIG["x_axis"]["step_size"]
STAGE = TESTCONFIG["x_axis"]["stage_type"]


INTERFACE = SerialInterfaceMock

PISTAGES = PIStagesInterface(
    port=TESTCONFIG["x_axis"]["port"],
    baud_rate=TESTCONFIG["x_axis"]["baud_rate"],
    interface=INTERFACE,
)


def test_init_motor():
    PISTAGES.init_motor(address=ADDRESS)
    assert PISTAGES.serial_interface._serial_commands[-3:] == [
        b"\x010MN\r",
        b"\x010RT\r",
        b"\x010SV200000\r",
    ]


def test_find_edge():
    def __get_position(self, address):
        # Blank get Position function
        return 0

    func_type = type(PISTAGES._get_position)
    PISTAGES._get_position = func_type(__get_position, PISTAGES)
    PISTAGES.find_edge(address=ADDRESS, unit=UNIT, stage=STAGE, step_size=STEPSIZE)
    assert PISTAGES.serial_interface._serial_commands[-1] == b"\x010FE0\r"


def test_set_home() -> None:
    PISTAGES.set_home(address=ADDRESS)
    assert PISTAGES.serial_interface._serial_commands[-1] == b"\x010DH\r"


def test_go_home() -> None:
    PISTAGES.go_home(address=ADDRESS)
    assert PISTAGES.serial_interface._serial_commands[-1] == b"\x010GH\r"


def test_abort():
    PISTAGES.abort(address=ADDRESS)
    assert PISTAGES.serial_interface._serial_commands[-1] == b"\x010AB\r"


def test_move_to_position():
    PISTAGES.move_to_position(
        address=ADDRESS, amount="0", unit=UNIT, stage=STAGE, step_size=STEPSIZE
    )
    assert PISTAGES.serial_interface._serial_commands[-1] == b"\x010MA0\r"


def test_move_relative():
    PISTAGES.move_relative(
        address=ADDRESS, amount="0", unit=UNIT, stage=STAGE, step_size=STEPSIZE
    )
    assert PISTAGES.serial_interface._serial_commands[-1] == b"\x010MR0\r"


def test_get_position():
    def __get_position(self, address):
        # Blank get Position function
        return 0

    func_type = type(PISTAGES._get_position)
    PISTAGES._get_position = func_type(__get_position, PISTAGES)
    assert (
        PISTAGES.get_position(
            address=ADDRESS, unit=UNIT, stage=STAGE, step_size=STEPSIZE
        )
        == "0.000"
    )


if __name__ == "__main__":
    pytest.main()
