from abc import *

from sensor.SensorType import SensorType


class Sensor(metaclass=ABCMeta):
    INTERRUPT_MSG = 'interrupt'

    def __init__(self, sensorcate=None, sensorname=None, manager=None):
        self.manager = manager
        self.sensorType = SensorType.NONE
        self.sensorCategory=sensorcate
        self.sensorName=sensorname

        self.data = None

    def _setSensorType(self, stype):
        self.sensorType = stype

    def addData(self, data):
        self.data.put(data)

    def getDataQueue(self):
        return self.data

    def addManager(self, manager):
        self.manager = manager
        self.__setupData()

    def __setupData(self):
        if self.manager is not None:
            self.data = self.manager.Queue()

    def DisconnectLogs(self):
        self.data.put(self.INTERRUPT_MSG)