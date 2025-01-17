import logging
from motor_stage_ui import logger


class SerialInterfaceMock:
    def __init__(
        self,
        port: str,
        baud_rate: int = 9600,
        parity: str = "N",
        terminator: str = "\r",
        timeout: float = 2,
        stopbits: float = 2,
    ):

        self._serial_commands = []

        self.log = logger.setup_main_logger(__class__.__name__, logging.WARNING)
        self._terminator = terminator

    def _write(self, command: str):
        """
        Write command to serial port

        Args:
            command (str): Address of the motorstage

        """
        msg = (command + self._terminator).encode()
        self.log.debug(msg)
        self._serial_commands.append(msg)

    def _read(self):
        """Read message from serial port.

        Returns:
            str: message
        """
        msg = self._serial_commands[-1].decode().strip().replace(self._terminator, "")
        if msg == "":
            self.log.error("No responds from serial interface.")
            raise ValueError
        return msg
