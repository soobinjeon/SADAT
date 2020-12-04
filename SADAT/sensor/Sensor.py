import math
from abc import *

import numpy as np

from sensor.SensorType import SensorType


class Sensor(metaclass=ABCMeta):
    INTERRUPT_MSG = 'interrupt'
    def __init__(self, sensorcate=None, sensorname=None):
        self.sensorType = SensorType.NONE
        self.sensorCategory=sensorcate
        self.sensorName=sensorname

        self.data = None

    def doWork(self, inputdata):
        self._doWorkDataInput(inputdata)
        self._doPostWork(inputdata)

    @abstractmethod
    def _doPostWork(self, inputdata):
        pass

    @abstractmethod
    def _doWorkDataInput(self, inputdata=None):
        pass

    def _setSensorType(self, stype):
        self.sensorType = stype

    def addData(self, data):
        self.data.put(data)

    def getDataQueue(self):
        return self.data

    def setupDataManager(self, manager):
        if manager is not None:
            self.data = manager.Queue()

    def DisconnectLogs(self):
        self.data.put(self.INTERRUPT_MSG)

    def _inputdataArray(self, data):
        tx, ty = self.__getCoordinatebyLidarNP(distance=data.distance, angle=data.angle)
        return tx.tolist(), ty.tolist()
        #tempx.append(tx)
        #tempy.append(ty)

    def _inputdata(self, data, tempx, tempy):
        distance = data['distance']
        angle = data['angle']
        sflag = data['start_flag']
        tx, ty = self.__getCoordinatebyLidar(distance=distance, angle=angle)
        tempx.append(tx)
        tempy.append(ty)

    def __getCoordinatebyLidar(self, distance, angle):
        x = distance * math.cos(math.radians(90 - angle))
        y = -1 * (distance * math.sin(math.radians(90 - angle)))

        return x, y

    def __getCoordinatebyLidarNP(self, distance, angle):
        x = distance * np.cos(np.radians(90 - angle))
        y = -1 * (distance * np.sin(np.radians(90 - angle)))
        return x, y