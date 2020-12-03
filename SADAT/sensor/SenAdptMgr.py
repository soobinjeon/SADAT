from sensor.psensor.RPLidar2D import RPLidar2D
from sensor.vsensor.RPLidar2Dv import RPLidar2Dv
from sensor.vsensor.Track import Track


class SenAdptMgr:
    def __init__(self, srcmanager, manager):
        self.srcmanager = srcmanager
        self.manager = manager
        self.__initDevices()

    def __initDevices(self):
        #actual Device
        self.__addActualSensor(RPLidar2D())

        #virtual Device
        #self.__addVirtualSensor(Track())
        self.__addVirtualSensor(RPLidar2Dv())

    def __addActualSensor(self, sensor):
        self.srcmanager.addActualSensor(sensor, self.manager)

    def __addVirtualSensor(self, sensor):
        self.srcmanager.addVirtualSensor(sensor, self.manager)