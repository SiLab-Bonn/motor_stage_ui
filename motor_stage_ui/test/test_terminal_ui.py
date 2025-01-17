from click.testing import CliRunner
import motor_stage_ui.motor_stage_terminal as terminal_ui


def test_motor():
    runner = CliRunner()
    runner.invoke(terminal_ui.motor)


def test_init():
    runner = CliRunner()
    runner.invoke(terminal_ui.init)


def test_gohome():
    runner = CliRunner()
    runner.invoke(terminal_ui.gohome, ["x_axis"])


def test_pos():
    runner = CliRunner()
    runner.invoke(terminal_ui.pos, ["x_axis"])


def test_move():
    runner = CliRunner()
    runner.invoke(terminal_ui.move, ["-a 3cm x_axis"])
