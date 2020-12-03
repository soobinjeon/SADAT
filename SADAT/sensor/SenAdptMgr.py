from sensor.psensor.RPLidar2D import RPLidar2D
from sensor.vsensor.Track import Track


class SenAdptMgr:
    def __init__(self, srcmanager):
        self.srcmanager = srcmanager

        self.__initDevices()

    def __initDevices(self):
        #actual Device
        self.srcmanager.addActualSensor(RPLidar2D())

        #virtual Device
        self.srcmanager.addVirtualSensor(Track())