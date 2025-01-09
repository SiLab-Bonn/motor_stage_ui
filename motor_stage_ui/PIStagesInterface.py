import serial
from threading import Lock
import time
from pint import UnitRegistry
import logging
from motor_stage_ui import logger

# sudo chown :usr /dev/ttyUSB0


class PIStagesInterface:
    def __init__(
        self,
        port: str,
        baud_rate: int = 9600,
        parity: str = "N",
        terminator: str = "\r",
        timeout: float = 2,
        stopbits: float = 2,
    ):
        self._serial = serial.Serial(
            port=port,
            baudrate=baud_rate,
            parity=parity,
            timeout=timeout,
            stopbits=stopbits,
        )
        self.log = logger.setup_main_logger(__class__.__name__, logging.WARNING)
        self.ureg = UnitRegistry()
        self._terminator = terminator
        self._lock = Lock()

    # Serial helper functions

    def _write(self, command: str):
        """
        Write command to serial port

        Args:
            command (str): Address of the motorstage

        """
        with self._lock:
            msg = (command + self._terminator).encode()
            self.log.debug(msg)
            self._serial.write(msg)

    def _write_command(self, command: str, address: int = None):
        """Encodes the command for the PI motor stages.
        This includes a header '01' and an address to select the specific stage and deselect the others and the command.

        Args:
            command (str): Command for the stage
            address (int, optional): Address of the specific motor stage. Defaults to None.
        """
        if address:
            self._write(("\x01%d" % (address - 1)) + command)
        else:
            self.log.error("Commands needs motor address")

    def _read(self):
        """Read message from serial port.

        Returns:
            str: message
        """
        msg = (
            self._serial.read_until(self._terminator.encode())
            .decode()
            .strip(self._terminator)
        )
        if msg == "":
            self.log.error("No responds from motor controller.")
            raise ValueError
        return msg

    def _write_read(self, command: str, address: int = None):
        """Write command to port and read back answer.

        Args:
            command (str): Command for port
            address (int, optional): Address of specific motor stage. Defaults to None.

        Returns:
            _type_: Answer message
        """
        if address:
            self._write(("\x01%d" % (address - 1)) + command)
        else:
            self.log.error("Commands needs motor address")
        return self._read()

    # Motor stage commands

    def init_motor(self, address: int, logic: str = None) -> None:
        """Initialize motor stage. Powering and resetting the motor.
        This function needs poss. changes depending on the hardware specific.
        Check logic low or high of controller and motor stage speed if needed.

        Args:
            address (int): Address of the motor stage
            logic (str, optional): Specify logic can be 'low' or 'high'. Defaults to None.
        """
        self.motor_on(address=address)
        time.sleep(0.1)
        self._write_command("RT", address=address)
        time.sleep(0.1)

        if logic == "low":
            self._write_command("LL", address=address)  # set logic
            time.sleep(0.1)
        elif logic == "high":
            self._write_command("HL", address=address)  # set logic
            time.sleep(0.1)

        # set motor stage velocity
        self.velocity = 200000  # allegedly in steps per second
        self.set_velocity(address, self.velocity)
        time.sleep(0.1)

        logging.info("Initialized motorstage with address: %i" % address)

    def motor_on(self, address=None):
        self._write_command("MN", address)

    def motor_off(self, address=None):
        self._write_command("MF", address)

    def set_velocity(self, address: int, velocity: int):
        """Set motorstage velocity.

        Args:
            address (int): Address of the motorstage
            velocity (int): Motorstage velocity is set allegedly as steps per second (This seems a bit random in tests.)
        """
        velocity = "SV" + str(velocity)
        self._write_command(velocity, address=address)

    def find_edge(self, address: int, edge: int = 0) -> None:
        """Tries to move the motorstage to a edge.

        Args:
            address (int): Address of the motorstage
            edge (int, optional): edge of the stage set 0 or 1. Defaults to 0.
        """
        self._write_command("FE%d" % edge, address)
        pos = self._wait(address)
        self.log.warning("Edge found at position: {pos}".format(pos=pos))

    def set_home(self, address: int) -> None:
        """Set the current position of the motorstage as new 0.

        Args:
            address (int): Address of the motorstage
        """
        self._write_command("DH", address)
        self.log.info("Set Home for motorstage with address: %i" % (address))

    def go_home(self, address: int) -> None:
        """Moves the motorstage to the absolute zero position.

        Args:
            address (int): Address of the motorstage
        """
        self._write_command("GH", address)
        self.log.info("Go Home for motorstage with address: %i" % (address))

    def get_stat(self, address: int) -> None:
        """Logs status of the motor stage to the terminal. This also resets status register.

        Args:
            address (int): Address of the motorstage
        """
        err_msg = self._write_read("TS", address)
        self.log.warning(
            "Status of motor stage with address %i: %s" % (address, err_msg)
        )

    def abort(self, address: int) -> None:
        """Stops all movement of the motorstage.

        Args:
            address (int): Address of the motorstage
        """
        self._write_command("AB", address)
        self.log.info("Stop all movement motorstage with address: %i" % (address))

    def move_to_position(
        self, address: int, amount: str, unit: str, stage: str, step_size: float
    ) -> None:
        """Moves the motor stage absolute position.
        Accepts string inputs with units (4cm, -2mm...). If no unit is given, the motor moves the default unit amount.
        The unit inputs are converted using the pint package into the according motor controller steps.
        Careful stepsize depends on motorstage and powering. Deviations can also occur from weight on stage usw.

        Args:
            address (int): Address of the motorstage
            amount (str): absolute position
            unit (str): input unit
            stage (int): stage type either 'rotation' or translation
            step_size (float): step size of the motorstage given in deg or um respectively
        """
        try:
            if amount != "" and stage in ["translation", "rotation"]:
                pos = self._calculate_value(amount, unit, stage, step_size)
                self._move_to_position(address, int(pos))
            else:
                self.log.warning("Invalid stage type")
        except:
            self.log.warning("Invalid amount input")

    def move_relative(
        self, address: int, amount: str, unit: str, stage: str, step_size: float
    ) -> None:
        """Moves the motor stage relative amount, positive values for ahead, negatives for back.
        Accepts string inputs with units (4cm, -2mm...). If no unit is given, the motor moves the default unit amount.
        The unit inputs are converted using the pint package into the according motor controller steps.
        Careful stepsize depends on motorstage and powering. Deviations can also occur from weight on stage usw.

        Args:
            address (int): Address of the motorstage
            amount (str): absolute position
            unit (str): input unit
            stage (int): stage type either 'rotation' or translation
            step_size (float): step size of the motorstage given in deg or um respectively
        """
        try:
            if amount != "" and stage in ["translation", "rotation"]:
                pos = self._calculate_value(amount, unit, stage, step_size)
                self._move_relative(address, int(pos))
            else:
                self.log.warning("Invalid stage type")
        except:
            self.log.warning("Invalid amount input")

    def get_position(
        self, address: int, unit: str, stage: str, step_size: float
    ) -> str:
        """Get current position of the motorstage in units

        Args:
            address (int): Address of the motorstage
            unit (str): output unit
            stage (int): stage type either 'rotation' or translation
            step_size (int): step size of the motorstage given in deg or um

        Returns:
            str: current position of motorstage in unit 3 digits precision respectively
        """
        if stage in ["translation", "rotation"]:
            if stage == "translation":
                pos = self._get_position(address) * step_size * self.ureg.micrometer
                return "%.3f" % (pos.to(unit).magnitude)
            if stage == "rotation":
                pos = self._get_position(address) * step_size * self.ureg.deg
                return "%.3f" % (pos.to(unit).magnitude)
        else:
            self.log.warning("Invalid stage type")

    def _move_to_position(self, address: int, value: int) -> None:
        """Helper function for basil

        Args:
            address (int): Address of the motorstage
            value (int): move amount
        """
        self._write_command("MA%d" % value, address)
        self.log.info(
            "Move to position %i motorstage with address: %i" % (value, address)
        )

    def _move_relative(self, address: int, value: int = 1000000) -> None:
        """Helper function for basil

        Args:
            address (int): Address of the motorstage
            value (int): move amount
        """
        self._write_command("MR%d" % value, address)
        self.log.info(
            "Moved motorstage relative %i with address: %i" % (value, address)
        )

    def _get_position(self, address: int) -> None:
        """Helper function for basil

        Args:
            address (int): Address of the motorstage

        Returns:
            int: current position of motorstage in integer step sizes
        """
        try:
            msg = int(
                self._write_read("TP", address)[3:].replace("+", "").replace(":", "")
            )
        except ValueError:
            self.log.error(
                "Invalid motor stage responds:, check addresses, baudrate..."
            )
            raise ValueError
        return msg

    def _calculate_value(
        self, amount: str, unit: str, stage: str, step_size: float
    ) -> int:
        """Calculates number of motor steps from a given input amount and the given units

        Args:
            amount (str): Input amount
            unit (str): default unit to convert
            stage (str): stagetype
            step_size (float): hardware specific step size

        Returns:
            int: Number of motor steps.
        """
        if stage == "translation":
            try:
                pos = self.ureg(amount).to("um").magnitude / step_size
            except:
                pos = self.ureg(amount + unit).to("um").magnitude / step_size
        if stage == "rotation":
            try:
                pos = self.ureg(amount).to("deg").magnitude / step_size
            except:
                pos = self.ureg(amount + unit).to("deg").magnitude / step_size
        return pos
