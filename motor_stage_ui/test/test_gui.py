from pathlib import Path
import pytest
from motor_stage_ui.motor_stage_gui import MainWindow
from motor_stage_ui.test.utils import SerialInterfaceMock
from PyQt5 import QtCore

FILEPATH = Path(__file__).parent
CONFIG_FILE = FILEPATH / "test_configuration.yaml"

INTERFACE = SerialInterfaceMock


@pytest.fixture
def app(qtbot):
    motor_gui = MainWindow(CONFIG_FILE, interface=INTERFACE)
    return motor_gui


def test_init_clicked(app):
    app.mouseClick(app.init_clicked, app.QtCore.Qt.MouseButton.LeftButton)
    assert app.motor.serial_interface._serial_commands[-3:] == [
        b"\x010MN\r",
        b"\x010RT\r",
        b"\x010SV200000\r",
    ]
