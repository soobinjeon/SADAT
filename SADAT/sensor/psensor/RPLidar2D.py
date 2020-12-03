from sensor.SensorCategory import SensorCategory
from sensor.pSensor import pSensor


class RPLidar2D(pSensor):
    def __init__(self):
        super().__init__(SensorCategory.Lidar2D, 'RPLidar A3')

    def doWorkDataInput(self, inputdata=None):
        pass