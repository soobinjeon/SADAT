import math
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

    def inputdata(self, data, tempx, tempy):
        distance = data['distance']
        angle = data['angle']
        sflag = data['start_flag']
        tx, ty = self.getCoordinatebyLidar(distance=distance, angle=angle)
        tempx.append(tx)
        tempy.append(ty)

    def getCoordinatebyLidar(self, distance, angle):
        x = distance * math.cos(math.radians(90 - angle))
        y = -1 * (distance * math.sin(math.radians(90 - angle)))

        return x, y