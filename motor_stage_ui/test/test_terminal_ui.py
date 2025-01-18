from click.testing import CliRunner
import os
import motor_stage_ui.motor_stage_terminal as terminal_ui


os.environ["TEST"] = "True"


def test_motor():
    runner = CliRunner()
    result = runner.invoke(terminal_ui.motor)
    assert result.exit_code == 0


def test_init():
    runner = CliRunner()
    result = runner.invoke(terminal_ui.motor, ["init", "x_axis"])
    assert result.exit_code == 0
    result = runner.invoke(terminal_ui.motor, ["init", "rot"])
    assert result.exit_code == 0


def test_move():
    runner = CliRunner()
    result = runner.invoke(terminal_ui.motor, ["move", "-a", "2cm", "x_axis"])
    assert result.exit_code == 0
    result = runner.invoke(terminal_ui.motor, ["move", "-a", "2deg", "rot"])
    assert result.exit_code == 0


def test_moveto():
    runner = CliRunner()
    result = runner.invoke(terminal_ui.motor, ["moveto", "-a", "-1cm", "x_axis"])
    assert result.exit_code == 0
    result = runner.invoke(terminal_ui.motor, ["moveto", "-a", "-1deg", "rot"])
    assert result.exit_code == 0


def test_pos():
    runner = CliRunner()
    result = runner.invoke(terminal_ui.motor, ["pos", "x_axis"])
    assert result.exit_code == 0
    assert result.output == "Position of: x_axis 0.000 mm\n"
    result = runner.invoke(terminal_ui.motor, ["pos", "rot"])
    assert result.exit_code == 0
    assert result.output == "Position of: rot 0.000 deg\n"


def test_stop():
    runner = CliRunner()
    result = runner.invoke(terminal_ui.motor, ["stop", "x_axis"])
    assert result.exit_code == 0
    result = runner.invoke(terminal_ui.motor, ["stop", "rot"])
    assert result.exit_code == 0


def test_sethome():
    runner = CliRunner()
    result = runner.invoke(terminal_ui.motor, ["sethome", "x_axis"])
    assert result.exit_code == 0
    result = runner.invoke(terminal_ui.motor, ["sethome", "rot"])
    assert result.exit_code == 0


def test_gohome():
    runner = CliRunner()
    result = runner.invoke(terminal_ui.motor, ["gohome", "x_axis"])
    assert result.exit_code == 0
    result = runner.invoke(terminal_ui.motor, ["gohome", "rot"])
    assert result.exit_code == 0


def test_status():
    runner = CliRunner()
    result = runner.invoke(terminal_ui.motor, ["status", "x_axis"])
    assert result.exit_code == 0
    assert result.output == "Status of: x_axis \x010TS\n"
    result = runner.invoke(terminal_ui.motor, ["status", "rot"])
    assert result.exit_code == 0
    assert result.output == "Status of: rot \x012TS\n"
