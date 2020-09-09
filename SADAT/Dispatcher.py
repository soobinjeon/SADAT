from abc import *
from PyQt5.QtCore import pyqtSignal


class Dispatcher(metaclass=ABCMeta):

    def __init__(self, guiApp=None):
        self.guiApp = guiApp
        self.value = None
        self.vel = None

    def setValue(self, value):
        self.value = value

    def setVelocity(self, vel):
        self.vel = vel
        print("set Velocity - ", self.vel)

    def getEOFMessage(self):
        return 'interrupt'

    @abstractmethod
    def dispatch(self):
        pass