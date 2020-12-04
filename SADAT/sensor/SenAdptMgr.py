from enum import Enum
from sensor.psensor.RPLidar2D import RPLidar2DA3
from sensor.vsensor.RPLidar2Dv import RPLidar2Dv
from sensor.vsensor.Track import Track

class AttachedSensorName(Enum):
    RPLidar2DA3 = 1
    RPLidar2DVirtual = 2
    Tracker1 = 3

class SenAdptMgr:
    def __init__(self, srcmanager, manager):
        self.srcmanager = srcmanager
        self.manager = manager
        self.__initDevices()

    def __initDevices(self):
        #actual Device
        self.__addActualSensor(RPLidar2DA3(AttachedSensorName.RPLidar2DA3))

        #virtual Device
        self.__addVirtualSensor(Track(AttachedSensorName.Tracker1))
        self.__addVirtualSensor(RPLidar2Dv(AttachedSensorName.RPLidar2DVirtual))

    def __addActualSensor(self, sensor):
        self.srcmanager.addActualSensor(sensor, self.manager)

    def __addVirtualSensor(self, sensor):
        self.srcmanager.addVirtualSensor(sensor, self.manager)