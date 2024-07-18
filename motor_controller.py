import time
from basil.dut import Dut
import logger
import logging

# sudo chown :usr /dev/ttyUSB0

class MotorController(object):
    def __init__(self) -> None:
        self.log = logger.setup_main_logger(__class__.__name__, logging.DEBUG)
        self.dut = Dut('<path to>/mercury_pyserial.yaml')
        self.dut.init()
        
    def init_motor(self, address):
        self.dut["MotorStage"].motor_on(address=address)
        time.sleep(0.1)
        self.dut["MotorStage"]._write_command('RT', address=address)
        time.sleep(0.1)
        self.dut["MotorStage"].motor_command('SV100000', address=address)
        time.sleep(0.1)
        self.log.info('Inititialized motorstage with address: %i' %address)

    def move_relative(self, address, value=1000000):
        self.dut["MotorStage"].move_relative(address=address, value=value, wait=False)
        self.log.info('Moved motorstage relative %i with address: %i' %(value, address))

    def find_edge(self, address, edge=0):
        self.dut["MotorStage"].find_edge(1, address=address)

    def set_home(self, address):
        self.dut["MotorStage"].set_home(address=address)
        self.log.info('Set Home for motorstage with address: %i' %(address))

    def go_home(self, address):
        self.dut["MotorStage"].go_home(address=address)
        self.log.info('Go Home for motorstage with address: %i' %(address))

    def move_to_position(self, address, value):
        self.dut["MotorStage"].set_position(value, address=address, wait=False)
        self.log.info('Move to position %i motorstage with address: %i' %(value, address))

    def get_position(self, address):
        return self.dut["MotorStage"].get_position(address=address)

    def abort(self, address):
        self.dut["MotorStage"].abort(address=address)
        self.log.info('Stop all movement motorstage with address: %i' %(address))

if __name__ == '__main__':
    x = MotorController()
    x.move_relative(1, 1000000)
