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

        self.realtimeData = None
        self.storedData = None

    def doWork(self, inputdata):
        #self.__cleanstoredData()
        self._doWorkDataInput(inputdata)
        self._doPostWork(inputdata)

    @abstractmethod
    def _doPostWork(self, inputdata):
        pass

    @abstractmethod
    def _doWorkDataInput(self, inputdata=None):
        pass

    def __cleanstoredData(self):
        if self.storedData is not None:
            self.storedData = []

    def _setSensorType(self, stype):
        self.sensorType = stype

    def addRealtimeData(self, data):
        self.realtimeData.put(data)

    def getRealtimeDataQueue(self):
        return self.realtimeData

    def _addStoredData(self, inputdata):
        self.storedData.append(inputdata)

    def getStoredDataset(self):
        return self.storedData

    def setupDataManager(self, manager):
        if manager is not None:
            self.realtimeData = manager.Queue()
            self.storedData = manager.list()

    def DisconnectLogs(self):
        self.realtimeData.put(self.INTERRUPT_MSG)

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