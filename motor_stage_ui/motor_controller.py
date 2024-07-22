from basil.dut import Dut
import basil
from motor_stage_ui import logger

import os
from pint import UnitRegistry
import logging
import time

"""

Main motor controller class. Uses the basil mercury controller functions. 
Change baud rate and usb port of the motor stage in hte mercury_pyserial.yaml.

"""

# sudo chown :usr /dev/ttyUSB0


class MotorController(object):
    def __init__(self) -> None:
        self.log = logger.setup_main_logger(__class__.__name__, logging.DEBUG)
        self.ureg = UnitRegistry()
        path = os.path.dirname(basil.__file__)
        self.dut = Dut(path + "/../examples/lab_devices/mercury_pyserial.yaml")
        self.dut.init()

    def init_motor(self, address: int) -> None:
        """Initialize motor stage. Powering and resetting the motor.
        This function needs poss. changes depending on the hardware specific.
        Check logic low or high of controller and motor stage speed if needed.

        Args:
            address (int): Address of the motorstage
        """
        self.dut["MotorStage"].motor_on(address=address)
        time.sleep(0.1)
        self.dut["MotorStage"]._write_command("RT", address=address)
        time.sleep(0.1)
        # self.dut["MotorStage"].LL(address=address) # set logic
        # time.sleep(0.1)
        # self.dut["MotorStage"]._write_command('HL', address=address) # set logic
        # time.sleep(0.1)
        self.dut["MotorStage"]._write_command(
            "SV100000", address=address
        )  # set motor stage velocity
        time.sleep(0.1)
        self.log.info("Inititialized motorstage with address: %i" % address)

    def find_edge(self, address: int, edge: int = 0) -> None:
        """Tries to move the motorstage to a edge.

        Args:
            address (int): Address of the motorstage
            edge (int, optional): edge of the stage set 0 or 1. Defaults to 0.
        """
        self.dut["MotorStage"].find_edge(1, address=address)

    def set_home(self, address: int) -> None:
        """Set the current position of the motorstage as new 0.

        Args:
            address (int): Address of the motorstage
        """
        self.dut["MotorStage"].set_home(address=address)
        self.log.info("Set Home for motorstage with address: %i" % (address))

    def go_home(self, address: int) -> None:
        """Moves the motorstage to the absolut zero position.

        Args:
            address (int): Address of the motorstage
        """
        self.dut["MotorStage"].go_home(address=address)
        self.log.info("Go Home for motorstage with address: %i" % (address))

    def abort(self, address: int) -> None:
        """Stops all movement of the motorstage.

        Args:
            address (int): Address of the motorstage
        """
        self.dut["MotorStage"].abort(address=address)
        self.log.info("Stop all movement motorstage with address: %i" % (address))

    def move_to_position(
        self, address: int, amount: str, unit: str, stage: str, step_size: float
    ) -> None:
        """Moves the motor stage absolute position.
        Accepts string inputs with units (4cm, -2mm...). If no unit is given, the motor moves the default unit amount.
        The unit inputs are converted using the pint package into the according motor controller steps.
        Carefull stepsize depends on motorstage and powering. Deviations can also occure from weight on stage usw.

        Args:
            address (int): Address of the motorstage
            amount (str): absolute position
            unit (str): input unit
            stage (int): stage type eather 'rotation' or translation
            step_size (float): step size of the motorstage given in deg or um respectivly
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
        Carefull stepsize depends on motorstage and powering. Deviations can also occure from weight on stage usw.

        Args:
            address (int): Address of the motorstage
            amount (str): absolute position
            unit (str): input unit
            stage (int): stage type eather 'rotation' or translation
            step_size (float): step size of the motorstage given in deg or um respectivly
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
            stage (int): stage type eather 'rotation' or translation
            step_size (int): step size of the motorstage given in deg or um respectivly

        Returns:
            str: current position of motorstage in unit 3 digits precision
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
        self.dut["MotorStage"].set_position(value, address=address, wait=False)
        self.log.info(
            "Move to position %i motorstage with address: %i" % (value, address)
        )

    def _move_relative(self, address: int, value: int = 1000000) -> None:
        """Helper function for basil

        Args:
            address (int): Address of the motorstage
            value (int): move amount
        """
        self.dut["MotorStage"].move_relative(address=address, value=value, wait=False)
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
        return self.dut["MotorStage"].get_position(address=address)

    def _calculate_value(
        self, amount: str, unit: str, stage: str, step_size: float
    ) -> int:
        """Calculates number of motor steps from a given in put amount and the given units

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


if __name__ == "__main__":
    x = MotorController()
    x.move_relative(1, 1000000)
