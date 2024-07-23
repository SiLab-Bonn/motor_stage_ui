#!/usr/bin/env python3
from typing import Any, Tuple

from constellation.core.satellite import Satellite, SatelliteArgumentParser
from constellation.core.configuration import ConfigError, Configuration
from constellation.core.fsm import SatelliteState
from motor_stage_ui.motor_controller import MotorController
from constellation.core.commandmanager import cscp_requestable
from constellation.core.cscp import CSCPMessage
from constellation.core.base import setup_cli_logging


class MotorStage(Satellite):
    def do_initializing(self, config: Configuration) -> str:

        self.log.info(
            "Received configuration with parameters: %s",
            ", ".join(config.get_keys()),
        )
        self.stage = config["stage"]
        self.address = config["address"]
        self.step_size = eval(str(config["step_size"]))
        self.unit = config["unit"]
        try:
            self.device = MotorController()
            pass
        except KeyError as e:
            self.log.error(
                "Attribute '%s' is required but missing from the configuration.", e
            )
            raise ConfigError

        self.device.init_motor(config["address"])
        return "Initialized"

    @cscp_requestable
    def move(self, request: CSCPMessage) -> Tuple[str, str, None]:
        self.device.move_relative(
            self.address, request.payload, self.unit, self.stage, self.step_size
        )
        return "Moved", request.payload, None

    @cscp_requestable
    def moveto(self, request: CSCPMessage) -> Tuple[str, str, None]:
        self.device.move_to_position(
            self.address, request.payload, self.unit, self.stage, self.step_size
        )
        return "Moved to:", str(request.payload), None

    @cscp_requestable
    def stop(self, request: CSCPMessage) -> Tuple[str, str, None]:
        self.device.abort(self.address)
        return "Stopped", None, None

    @cscp_requestable
    def sethome(self, request: CSCPMessage) -> Tuple[str, str, None]:
        self.device.set_home(self.address)
        return "Set home", None, None

    @cscp_requestable
    def gohome(self, request: CSCPMessage) -> Tuple[str, str, None]:
        self.device.go_home(self.address)
        return "Go home", None, None

    @cscp_requestable
    def getpos(self, request: CSCPMessage) -> Tuple[str, str, None]:
        return (
            "Position",
            str(
                self.device.get_position(
                    self.address, self.unit, self.stage, self.step_size
                )
            ),
            None,
        )

    def _ready(self) -> bool:
        """From the FSM state, determine whether we are ready."""
        if self.fsm.current_state_value in [
            SatelliteState.NEW,
            SatelliteState.ERROR,
            SatelliteState.DEAD,
            SatelliteState.initializing,
            SatelliteState.reconfiguring,
        ]:
            return False
        return True


def main(args=None):

    parser = SatelliteArgumentParser(
        description=main.__doc__,
        epilog="This is a 3rd-party component of Constellation.",
    )
    parser.set_defaults(name="motor_stage")
    args = vars(parser.parse_args(args))

    setup_cli_logging(args["name"], args.pop("log_level"))

    s = MotorStage(**args)
    s.run_satellite()
