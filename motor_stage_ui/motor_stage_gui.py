from motor_stage_ui.PIStagesInterface import PIStagesInterface
from motor_stage_ui import logger
import motor_stage_ui

import yaml
import logging
from PyQt5.QtCore import QSize, Qt, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QLabel
import sys
import os

"""

GUI for the motor stage

"""


class MainWindow(QMainWindow):
    def __init__(self, config_path):
        super().__init__()

        self.log = logger.setup_main_logger(__class__.__name__, logging.DEBUG)
        with open(config_path, "r") as file:
            self.conf = yaml.full_load(file)

        self.setWindowTitle("Motor Stage")
        self.setFixedSize(QSize(1400, 500))

        timer = QTimer(self)
        self.pos = []
        self.motor = []
        for index, motor in enumerate(self.conf):
            self.motor.append(
                PIStagesInterface(
                    port=self.conf[motor]["port"],
                    baud_rate=self.conf[motor]["baud_rate"],
                )
            )
            stage = self.conf[motor]["stage_type"]
            address = self.conf[motor]["address"]
            step_size = eval(str(self.conf[motor]["step_size"]))
            unit = self.conf[motor]["unit"]
            # self.init_clicked(address)
            self.motor_gui(
                address,
                unit=unit,
                stage=stage,
                step_size=step_size,
                name=motor,
                index=index,
            )

            self.pos.append(
                self.position_setting(
                    address, unit=unit, stage=stage, step_size=step_size, index=index
                )
            )

            # really bad loop to connect the position button to a timer for positional update
            try:
                [
                    timer.timeout.connect(
                        lambda: self.pos[i].setText(
                            (
                                self.get_position_clicked(
                                    self.conf[list(self.conf.keys())[i]]["address"],
                                    unit=self.conf[list(self.conf.keys())[i]]["unit"],
                                    stage=self.conf[list(self.conf.keys())[i]][
                                        "stage_type"
                                    ],
                                    step_size=eval(
                                        str(
                                            self.conf[list(self.conf.keys())[i]][
                                                "step_size"
                                            ]
                                        )
                                    ),
                                    index=index,
                                )
                            )
                        )
                    )
                    for i in range(len(self.pos))
                ]
            except:
                self.log.warning("Could not get motor position!")
        timer.start(200)  # position update timer in ms
        self.labels()

    def position_setting(
        self,
        address: int = 1,
        unit: str = "mm",
        stage: str = "translation",
        step_size: float = 0.02,
        index=1,
    ) -> QPushButton:
        """Button display of the current position of the motor stage

        Args:
            address (int, optional): Address of the motorstage. Defaults to 1.
            unit (str, optional): Unit of output position. Defaults to 'mm'.
            stage (str, optional): Stage type. Defaults to 'translation'.
            step_size (float, optional): Step size of the motorstage in deg or um. Defaults to 0.2.

        Returns:
            QPushButton: Position button
        """
        position = QPushButton(text="Pos.", parent=self)
        position.setFixedSize(100, 30)
        position.setIconSize(QSize(40, 40))
        position.setGeometry(300, (index) * 30 + 20, 40, 40)
        position.clicked.connect(
            lambda: position.setText(
                (
                    self.get_position_clicked(
                        address, unit, stage, step_size, index=index
                    )
                )
            )
        )
        return position

    """ Draw GUI """

    def labels(self):
        """Draws labels above motorstage buttons."""
        label = QLabel("Motor", self)
        label.setAlignment(Qt.AlignCenter)
        label.resize(100, 20)
        label.move(0, 0)

        label = QLabel("Init.", self)
        label.setAlignment(Qt.AlignCenter)
        label.resize(100, 20)
        label.move(100, 0)

        label = QLabel("MV. Back", self)
        label.setAlignment(Qt.AlignCenter)
        label.resize(100, 20)
        label.move(200, 0)

        label = QLabel("Position", self)
        label.setAlignment(Qt.AlignCenter)
        label.resize(100, 20)
        label.move(300, 0)

        label = QLabel("MV. Ahead", self)
        label.setAlignment(Qt.AlignCenter)
        label.resize(100, 20)
        label.move(400, 0)

        label = QLabel("Stop", self)
        label.setAlignment(Qt.AlignCenter)
        label.resize(100, 20)
        label.move(500, 0)

        label = QLabel("Input rel.", self)
        label.setAlignment(Qt.AlignCenter)
        label.resize(100, 20)
        label.move(600, 0)

        label = QLabel("MV. rel.", self)
        label.setAlignment(Qt.AlignCenter)
        label.resize(100, 20)
        label.move(700, 0)

        label = QLabel("Input abs.", self)
        label.setAlignment(Qt.AlignCenter)
        label.resize(100, 20)
        label.move(800, 0)

        label = QLabel("MV. abs.", self)
        label.setAlignment(Qt.AlignCenter)
        label.resize(100, 20)
        label.move(900, 0)

        label = QLabel("Set Zero", self)
        label.setAlignment(Qt.AlignCenter)
        label.resize(100, 20)
        label.move(1000, 0)

        label = QLabel("MV. Zero", self)
        label.setAlignment(Qt.AlignCenter)
        label.resize(100, 20)
        label.move(1100, 0)

        label = QLabel("Input Notes", self)
        label.setAlignment(Qt.AlignCenter)
        label.resize(200, 20)
        label.move(1200, 0)

    def motor_gui(
        self,
        address: int = 1,
        unit: str = "mm",
        stage: str = "translation",
        step_size: float = 0.2,
        name: str = 1,
        index: int = 1,
    ):
        """Draws buttons of the motorstage

        Args:
            address (int, optional): Address of the motorstage. Defaults to 1.
            unit (str, optional): Unit of output position. Defaults to 'mm'.
            stage (str, optional): Stage type. Defaults to 'translation'.
            step_size (float, optional): Step size of the motorstage in deg or um. Defaults to 0.2.
            name (int, optional): Name of the motorstage. Defaults to 1.
        """
        name = QLineEdit(text=name, parent=self)
        name.move(0, index * 30 + 20)
        name.resize(100, 30)
        name.setAlignment(Qt.AlignCenter)

        init = QPushButton(text="init", parent=self)
        init.setFixedSize(100, 30)
        init.setIconSize(QSize(40, 40))
        init.setGeometry(100, (index) * 30 + 20, 40, 40)
        init.setStyleSheet("background-color : grey")
        init.setCheckable(True)
        init.clicked.connect(lambda: self.init_clicked(address, index))

        move_back = QPushButton(text="<<", parent=self)
        move_back.setFixedSize(100, 30)
        move_back.setIconSize(QSize(40, 40))
        move_back.setGeometry(200, (index) * 30 + 20, 40, 40)
        move_back.clicked.connect(
            lambda: self.move_back_clicked(address, unit, stage, step_size, index)
        )

        position = QPushButton(text="Pos.", parent=self)
        position.setFixedSize(100, 30)
        position.setIconSize(QSize(40, 40))
        position.setGeometry(300, (index) * 30 + 20, 40, 40)
        position.clicked.connect(
            lambda: position.setText(
                (self.get_position_clicked(address, unit, stage, step_size, index))
            )
        )

        move_ahead = QPushButton(text=">>", parent=self)
        move_ahead.setFixedSize(100, 30)
        move_ahead.setIconSize(QSize(40, 40))
        move_ahead.setGeometry(400, (index) * 30 + 20, 40, 40)
        move_ahead.clicked.connect(
            lambda: self.move_ahead_clicked(address, unit, stage, step_size, index)
        )

        abort = QPushButton(text="abort", parent=self)
        abort.setFixedSize(100, 30)
        abort.setIconSize(QSize(40, 40))
        abort.setGeometry(500, (index) * 30 + 20, 40, 40)
        abort.setStyleSheet("background-color : red")
        abort.clicked.connect(lambda: self.abort_clicked(address, index))

        position_input_rel = QLineEdit(parent=self)
        position_input_rel.resize(100, 30)
        position_input_rel.move(600, (index) * 30 + 20)
        position_input_rel.setAlignment(Qt.AlignCenter)

        set_position_rel = QPushButton(text="Go rel.", parent=self)
        set_position_rel.setFixedSize(100, 30)
        set_position_rel.setIconSize(QSize(40, 40))
        set_position_rel.setGeometry(700, (index) * 30 + 20, 40, 40)
        set_position_rel.clicked.connect(
            lambda: self.set_position_rel_clicked(
                address, position_input_rel.text(), unit, stage, step_size, index
            )
        )

        position_input_abs = QLineEdit(parent=self)
        position_input_abs.resize(100, 30)
        position_input_abs.move(800, (index) * 30 + 20)
        position_input_abs.setAlignment(Qt.AlignCenter)

        set_position_abs = QPushButton(text="Go abs.", parent=self)
        set_position_abs.setFixedSize(100, 30)
        set_position_abs.setIconSize(QSize(40, 40))
        set_position_abs.setGeometry(900, (index) * 30 + 20, 40, 40)
        set_position_abs.clicked.connect(
            lambda: self.set_position_abs_clicked(
                address, position_input_abs.text(), unit, stage, step_size, index
            )
        )

        set_home = QPushButton(text="Set Home", parent=self)
        set_home.setFixedSize(100, 30)
        set_home.setIconSize(QSize(40, 40))
        set_home.setGeometry(1000, (index) * 30 + 20, 40, 40)
        set_home.clicked.connect(lambda: self.set_home_clicked(address, index))

        go_home = QPushButton(text="Go Home", parent=self)
        go_home.setFixedSize(100, 30)
        go_home.setIconSize(QSize(40, 40))
        go_home.setGeometry(1100, (index) * 30 + 20, 40, 40)
        go_home.clicked.connect(lambda: self.go_home_clicked(address, index))

        notes = QLineEdit(text="Notes", parent=self)
        notes.move(1200, (index) * 30 + 20)
        notes.resize(200, 30)
        notes.setAlignment(Qt.AlignCenter)

    """ Button actions when clicked  """

    def init_clicked(self, address: int, index: int) -> None:
        self.motor[index].init_motor(address)

    def move_back_clicked(
        self, address: int, unit: str, stage: str, step_size: str, index: int
    ) -> None:
        self.motor[index].move_relative(address, "-1", unit, stage, step_size)

    def move_ahead_clicked(
        self, address: int, unit: str, stage: str, step_size: float, index: int
    ) -> None:
        self.motor[index].move_relative(address, "1", unit, stage, step_size)

    def abort_clicked(self, address: int, index: int) -> None:
        self.motor[index].abort(address)

    def set_home_clicked(self, address: int, index: int) -> None:
        self.motor[index].set_home(address)

    def go_home_clicked(self, address: int, index: int) -> None:
        self.motor[index].go_home(address)

    def set_position_abs_clicked(
        self,
        address: int,
        textbox: str,
        unit: str,
        stage: str,
        step_size: float,
        index: int,
    ) -> None:
        self.motor[index].move_to_position(address, textbox, unit, stage, step_size)

    def set_position_rel_clicked(
        self,
        address: int,
        textbox: str,
        unit: str,
        stage: str,
        step_size: float,
        index: int,
    ) -> None:
        self.motor[index].move_relative(address, textbox, unit, stage, step_size)

    def get_position_clicked(
        self, address: int, unit: str, stage: str, step_size: float, index: int
    ) -> str:
        return self.motor[index].get_position(address, unit, stage, step_size)


def main():
    app = QApplication(sys.argv)

    path = os.path.dirname(motor_stage_ui.__file__)
    window = MainWindow(path + "/configuration.yaml")
    window.show()

    app.exec()


if __name__ == "__main__":
    main()
