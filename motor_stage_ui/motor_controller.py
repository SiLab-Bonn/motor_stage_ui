from basil.dut import Dut
from motor_stage_ui import logger

from pint import UnitRegistry
import logging
import time

# sudo chown :usr /dev/ttyUSB0

class MotorController(object):
    def __init__(self) -> None:
        self.log = logger.setup_main_logger(__class__.__name__, logging.DEBUG)
        self.ureg = UnitRegistry()
        self.dut = Dut('<path to>/basil/examples/lab_devices/mercury_pyserial.yaml')
        self.dut.init()
        
    def init_motor(self, address):
        self.dut["MotorStage"].motor_on(address=address)
        time.sleep(0.1)
        self.dut["MotorStage"]._write_command('RT', address=address)
        # time.sleep(0.1)
        # self.dut["MotorStage"].LL(address=ad) # set logic
        time.sleep(0.1)
        self.dut["MotorStage"].motor_command('SV100000', address=address) #set motor stage velocity
        time.sleep(0.1)
        self.log.info('Inititialized motorstage with address: %i' %address)

    def find_edge(self, address, edge=0):
        self.dut["MotorStage"].find_edge(1, address=address)

    def set_home(self, address):
        self.dut["MotorStage"].set_home(address=address)
        self.log.info('Set Home for motorstage with address: %i' %(address))

    def go_home(self, address):
        self.dut["MotorStage"].go_home(address=address)
        self.log.info('Go Home for motorstage with address: %i' %(address))

    def abort(self, address):
        self.dut["MotorStage"].abort(address=address)
        self.log.info('Stop all movement motorstage with address: %i' %(address))

    def move_to_position(self, address, amount, unit, stage, step_size):
        try:
            if amount != '':
                if stage == 'translation':
                    try:
                        pos = self.ureg(amount).to('um').magnitude/step_size 
                    except:
                        pos = self.ureg(amount + unit).to('um').magnitude/step_size 
                    self._move_to_position(address, int(pos))
                if stage == 'rotation':
                    try:
                        pos = self.ureg(amount).to('deg').magnitude/step_size 
                    except:
                        pos = self.ureg(amount + unit).to('deg').magnitude/step_size 
                    self._move_to_position(address, int(pos))
        except:
            self.log.warning('Invalid amount Input')

    def move_relative(self, address, amount, unit, stage, step_size):
        try:
            if amount != '':
                if stage == 'translation':
                    try:
                        pos = self.ureg(amount).to('um').magnitude/step_size 
                    except:
                        pos = self.ureg(amount + unit).to('um').magnitude/step_size 
                    self._move_relative(address, int(pos))
                if stage == 'rotation':
                    try:
                        pos = self.ureg(amount).to('deg').magnitude/step_size 
                    except:
                        pos = self.ureg(amount + unit).to('deg').magnitude/step_size 
                    self._move_relative(address, int(pos))
        except:
            self.log.warning('Invalid amount Input')

    def get_position(self, address, unit, stage, step_size):
        if stage == 'translation':
            pos = self._get_position(address)*step_size * self.ureg.micrometer
            return '%.3f'%(pos.to(unit).magnitude)
        if stage == 'rotation':
            pos = self._get_position(address)*step_size * self.ureg.deg
            return '%.3f'%(pos.to(unit).magnitude)

    def _move_to_position(self, address, value):
        self.dut["MotorStage"].set_position(value, address=address, wait=False)
        self.log.info('Move to position %i motorstage with address: %i' %(value, address))

    def _move_relative(self, address, value=1000000):
        self.dut["MotorStage"].move_relative(address=address, value=value, wait=False)
        self.log.info('Moved motorstage relative %i with address: %i' %(value, address))

    def _get_position(self, address):
        return self.dut["MotorStage"].get_position(address=address)

if __name__ == '__main__':
    x = MotorController()
    x.move_relative(1, 1000000)
