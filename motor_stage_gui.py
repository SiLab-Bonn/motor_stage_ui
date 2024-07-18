from PyQt5.QtCore import QSize, Qt, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QLabel
import sys
from motor_controller import MotorController
from pint import UnitRegistry
import yaml
import logger
import logging

class MainWindow(QMainWindow):
    def __init__(self, config_path):
        super().__init__()

        self.log = logger.setup_main_logger(__class__.__name__, logging.DEBUG)
        with open(config_path, "r") as file:
            self.conf = yaml.full_load(file)

        self.setWindowTitle("Motor Stage")
        self.setFixedSize(QSize(1400, 500))

        self.ureg = UnitRegistry()
        self.motor = MotorController()

        timer = QTimer(self)
        self.pos = []
        for motor in self.conf:
            stage = self.conf[motor]['stage']
            address = self.conf[motor]['address']
            step_size = eval(str(self.conf[motor]['step_size']))
            unit = self.conf[motor]['unit']
            self.motor_gui(address, unit=unit, stage=stage, step_size=step_size, name=motor)

            self.pos.append(self.position_setting(address, unit=unit, stage=stage, step_size=step_size))

            # really bad loop to connect the position button to a timer for positional update
            [timer.timeout.connect(lambda: self.pos[i].setText((self.get_position_clicked(self.conf[list(self.conf.keys())[i]]['address'], 
                                                                                          unit=self.conf[list(self.conf.keys())[i]]['unit'], 
                                                                                stage=self.conf[list(self.conf.keys())[i]]['stage'], 
                                                                                step_size=eval(str(self.conf[list(self.conf.keys())[i]]['step_size'])))))) 
                                                                                for i in range(len(self.pos))]
        timer.start(200) # position update timer in ms
        self.labels()

    def position_setting(self, address=1, unit='mm', stage='translation', step_size=0.2):
        position = QPushButton(text='Pos.', parent=self)
        position.setFixedSize(100, 30)
        position.setIconSize(QSize(40, 40))
        position.setGeometry(300, (address-1)*30+20, 40, 40)
        position.clicked.connect(lambda: position.setText((self.get_position_clicked(address, unit, stage, step_size))))
        return position

    def labels(self):
        label = QLabel('Motor', self)
        label.setAlignment(Qt.AlignCenter)
        label.resize(100, 20)  
        label.move(0, 0)

        label = QLabel('Init.', self)
        label.setAlignment(Qt.AlignCenter)
        label.resize(100, 20)  
        label.move(100, 0)

        label = QLabel('MV. Back', self)
        label.setAlignment(Qt.AlignCenter)
        label.resize(100, 20)  
        label.move(200, 0)

        label = QLabel('Position', self)
        label.setAlignment(Qt.AlignCenter)
        label.resize(100, 20)  
        label.move(300, 0)

        label = QLabel('MV. Ahead', self)
        label.setAlignment(Qt.AlignCenter)
        label.resize(100, 20)  
        label.move(400, 0)

        label = QLabel('Stop', self)
        label.setAlignment(Qt.AlignCenter)
        label.resize(100, 20)  
        label.move(500, 0)

        label = QLabel('Input rel.', self)
        label.setAlignment(Qt.AlignCenter)
        label.resize(100, 20)  
        label.move(600, 0)

        label = QLabel('MV. rel.', self)
        label.setAlignment(Qt.AlignCenter)
        label.resize(100, 20)  
        label.move(700, 0)

        label = QLabel('Input abs.', self)
        label.setAlignment(Qt.AlignCenter)
        label.resize(100, 20)  
        label.move(800, 0)

        label = QLabel('MV. abs.', self)
        label.setAlignment(Qt.AlignCenter)
        label.resize(100, 20)  
        label.move(900, 0)

        label = QLabel('Set Zero', self)
        label.setAlignment(Qt.AlignCenter)
        label.resize(100, 20)  
        label.move(1000, 0)

        label = QLabel('MV. Zero', self)
        label.setAlignment(Qt.AlignCenter)
        label.resize(100, 20)  
        label.move(1100, 0)

        label = QLabel('Input Notes', self)
        label.setAlignment(Qt.AlignCenter)
        label.resize(200, 20)  
        label.move(1200, 0)

    def motor_gui(self, address=1, unit='mm', stage='translation', step_size=0.2, name=1):
        name = QLineEdit(text=name, parent=self)
        name.move(0, (address-1)*30+20)
        name.resize(100, 30)
        name.setAlignment(Qt.AlignCenter) 

        init = QPushButton(text='init', parent=self)
        init.setFixedSize(100, 30)
        init.setIconSize(QSize(40, 40))
        init.setGeometry(100, (address-1)*30+20, 40, 40)
        init.setStyleSheet("background-color : grey")
        init.setCheckable(True)
        init.clicked.connect(lambda: self.init_clicked(address))

        move_back = QPushButton(text='<<', parent=self)
        move_back.setFixedSize(100, 30)
        move_back.setIconSize(QSize(40, 40))
        move_back.setGeometry(200, (address-1)*30+20, 40, 40)
        move_back.clicked.connect(lambda: self.move_back_clicked(address))

        position = QPushButton(text='Pos.', parent=self)
        position.setFixedSize(100, 30)
        position.setIconSize(QSize(40, 40))
        position.setGeometry(300, (address-1)*30+20, 40, 40)
        position.clicked.connect(lambda: position.setText((self.get_position_clicked(address, unit, stage, step_size))))

        move_ahead = QPushButton(text='>>', parent=self)
        move_ahead.setFixedSize(100, 30)
        move_ahead.setIconSize(QSize(40, 40))
        move_ahead.setGeometry(400, (address-1)*30+20, 40, 40)
        move_ahead.clicked.connect(lambda: self.move_ahead_clicked(address))

        abort = QPushButton(text='abort', parent=self)
        abort.setFixedSize(100, 30)
        abort.setIconSize(QSize(40, 40))
        abort.setGeometry(500, (address-1)*30+20, 40, 40)
        abort.setStyleSheet("background-color : red")
        abort.clicked.connect(lambda: self.abort_clicked(address))

        position_input_rel = QLineEdit(parent=self)
        position_input_rel.resize(100, 30)
        position_input_rel.move(600, (address-1)*30+20)
        position_input_rel.setAlignment(Qt.AlignCenter) 

        set_position_rel = QPushButton(text='Go rel.', parent=self)
        set_position_rel.setFixedSize(100, 30)
        set_position_rel.setIconSize(QSize(40, 40))
        set_position_rel.setGeometry(700, (address-1)*30+20, 40, 40)
        set_position_rel.clicked.connect(lambda: self.set_position_rel_clicked(address, position_input_rel.text(), unit, stage, step_size))

        position_input_abs = QLineEdit(parent=self)
        position_input_abs.resize(100,30)
        position_input_abs.move(800, (address-1)*30+20)
        position_input_abs.setAlignment(Qt.AlignCenter) 

        set_position_abs = QPushButton(text='Go abs.', parent=self)
        set_position_abs.setFixedSize(100, 30)
        set_position_abs.setIconSize(QSize(40, 40))
        set_position_abs.setGeometry(900, (address-1)*30+20, 40, 40)
        set_position_abs.clicked.connect(lambda: self.set_position_abs_clicked(address, position_input_abs.text(), unit, stage, step_size))

        set_home = QPushButton(text='Set Home', parent=self)
        set_home.setFixedSize(100, 30)
        set_home.setIconSize(QSize(40, 40))
        set_home.setGeometry(1000, (address-1)*30+20, 40, 40)
        set_home.clicked.connect(lambda: self.set_home_clicked(address))

        go_home = QPushButton(text='Go Home', parent=self)
        go_home.setFixedSize(100, 30)
        go_home.setIconSize(QSize(40, 40))
        go_home.setGeometry(1100, (address-1)*30+20, 40, 40)
        go_home.clicked.connect(lambda: self.go_home_clicked(address))

        notes = QLineEdit(text='Notes', parent=self)
        notes.move(1200, (address-1)*30+20)
        notes.resize(200, 30)
        notes.setAlignment(Qt.AlignCenter) 

    def init_clicked(self, address):
        self.motor.init_motor(address)

    def move_back_clicked(self, address):
        self.motor.move_relative(address, value=-10000)

    def move_ahead_clicked(self, address):
        self.motor.move_relative(address, value=10000)

    def abort_clicked(self, address):
        self.motor.abort(address)

    def set_home_clicked(self, address):
        self.motor.set_home(address)

    def go_home_clicked(self, address):
        self.motor.go_home(address)

    def set_position_abs_clicked(self, address, textbox, unit, stage, step_size):
        try:
            if textbox != '':
                if stage == 'translation':
                    try:
                        pos = self.ureg(textbox).to('um').magnitude/step_size 
                    except:
                        pos = self.ureg(textbox + unit).to('um').magnitude/step_size 
                    self.motor.move_to_position(address, int(pos))
                if stage == 'rotation':
                    try:
                        pos = self.ureg(textbox).to('deg').magnitude/step_size 
                    except:
                        pos = self.ureg(textbox + unit).to('deg').magnitude/step_size 
                    self.motor.move_to_position(address, int(pos))
        except:
            self.log.warning('Wrong Input')

    def set_position_rel_clicked(self, address, textbox, unit, stage, step_size):
        try:
            if textbox != '':
                if stage == 'translation':
                    try:
                        pos = self.ureg(textbox).to('um').magnitude/step_size 
                    except:
                        pos = self.ureg(textbox + unit).to('um').magnitude/step_size 
                    self.motor.move_relative(address, int(pos))
                if stage == 'rotation':
                    try:
                        pos = self.ureg(textbox).to('deg').magnitude/step_size 
                    except:
                        pos = self.ureg(textbox + unit).to('deg').magnitude/step_size 
                    self.motor.move_relative(address, int(pos))
        except:
            self.log.warning('Wrong Input')
        

    def get_position_clicked(self, address, unit, stage, step_size):
        if stage == 'translation':
            pos = self.motor.get_position(address)*step_size * self.ureg.micrometer
            return '%.3f'%(pos.to(unit).magnitude)
        if stage == 'rotation':
            pos = self.motor.get_position(address)*step_size * self.ureg.deg
            return '%.3f'%(pos.to(unit).magnitude)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow('configuration.yaml')
    window.show()

    app.exec()
