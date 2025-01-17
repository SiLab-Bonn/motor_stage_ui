from pathlib import Path
import os
import pytest
import yaml
from motor_stage_ui.pi_stages_interface import PIStagesInterface
from motor_stage_ui.pi_stages_interface import SerialInterface
from motor_stage_ui.tests.utils import SerialInterfaceMock


FILEPATH = Path(__file__).parent
CONFIG_FILE = FILEPATH / "test_configuration.yaml"

with open(CONFIG_FILE) as yaml_file:
    TESTCONFIG = yaml.safe_load(yaml_file)
ADDRESS = TESTCONFIG["x_axis"]["address"]
UNIT = TESTCONFIG["x_axis"]["unit"]
STEPSIZE = TESTCONFIG["x_axis"]["step_size"]
STAGE = TESTCONFIG["x_axis"]["stage_type"]

try:
    MOCK = not os.environ["HW"] == "True"
except KeyError:
    MOCK = True

if MOCK:
    INTERFACE = SerialInterfaceMock
else:
    INTERFACE = SerialInterface

PISTAGES = PIStagesInterface(
    port=TESTCONFIG["x_axis"]["port"],
    baud_rate=TESTCONFIG["x_axis"]["baud_rate"],
    interface=INTERFACE,
)


def test_init_motor():
    PISTAGES.init_motor(address=ADDRESS)
    if MOCK:
        assert PISTAGES.serial_interface._read() == [
            "\x010MN",
            "\x010RT",
            "\x010SV200000",
        ]


if __name__ == "__main__":
    pytest.main()
