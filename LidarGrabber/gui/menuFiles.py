from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import qApp, QAction, QMainWindow

from gui.menuItem import MenuItem
from simMode import Mode


class menuLoadSim(QAction):

    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.parent = parent
        self.triggered.connect(self.trig)
        self.setShortcut('Ctrl+S')
        self.setStatusTip('Exit application')

    def trig(self):
        self.parent.simulator.setAction(Mode.MODE_SIM)
        print("PlaySim")

class menuLogPlay(QAction):

    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.parent = parent
        self.triggered.connect(self.trig)
        self.setShortcut('Ctrl+L')
        self.setStatusTip('Logging')

    def trig(self):
        self.parent.simulator.setAction(Mode.MODE_LOG)
        print("PlayLogging")