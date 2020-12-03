from sensor.Sensor import Sensor
from sensor.SensorType import SensorType


class pSensor(Sensor):
    def __init__(self, sensorcate=None, sensorname=None):
        super().__init__(sensorcate, sensorname)
        self._setSensorType(SensorType.ActualSensor)
