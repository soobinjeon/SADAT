from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import qApp, QAction, QMainWindow

from gui.menuItem import MenuItem
from simMode import Mode


class menuSim(QAction):

    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.parent = parent
        self.triggered.connect(self.trig)
        self.setShortcut('Ctrl+P')
        self.setStatusTip('Exit application')

    def trig(self):
        #self.parent.playMode()
        self.parent.simulator.playMode()
        print("PlaySim")
