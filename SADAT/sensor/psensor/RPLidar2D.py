from sensor.SensorCategory import SensorCategory
from sensor.pSensor import pSensor


class RPLidar2DA3(pSensor):
    def __init__(self, name):
        super().__init__(SensorCategory.RPLidar2D, name)

    def _doWorkDataInput(self, inputdata):
        pass