from abc import *

from sensor.Sensor import Sensor
from sensor.SensorType import SensorType


class vSensor(Sensor):
    def __init__(self, sensorcate=None, sensorname=None):
        super().__init__(sensorcate, sensorname)
        self._setSensorType(SensorType.VirtualSensor)

    def _doPostWork(self, inputdata):
        pass

    def _addSimData(self, inputdata):
        self._addStoredData(inputdata)
