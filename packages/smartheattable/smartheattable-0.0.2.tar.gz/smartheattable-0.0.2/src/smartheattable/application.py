import sys

from PySide6.QtWidgets import (QApplication, QMainWindow, QButtonGroup)
from smartheattable.gui.ui_mainwindow import Ui_MainWindow
import logging


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.modegroup = QButtonGroup(self)
        self.modegroup.addButton(self.ui.rbLOPF, 0)
        self.modegroup.addButton(self.ui.rbLPF, 1)
        self.modegroup.addButton(self.ui.rbPF, 2)
        self.modegroup.setExclusive(True)
        self.modegroup.idClicked.connect(self.set_mode)
        self.ui.rbLOPF.click()
        print(f"Mode: {self.mode}")

    # mode commands
    def set_mode(self, button_id):
        match button_id:
            case 0:
                print("Setting mode to Linear Optimal Power Flow (LOPF)")
                self.mode = "LOPF"
            case 1:
                print("Setting mode to Linear Power Flow (LPF)")
                self.mode = "LPF"
            case 2:
                print("Setting mode to Power Flow (PF)")
                self.mode = "PF"
            case _:
                print("Mode is not defined")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName('Hancse Smart Scratch')
    window = MainWindow()
    window.setWindowTitle('Hancse Smart Scratch')
    window.show()
    app.exec()
