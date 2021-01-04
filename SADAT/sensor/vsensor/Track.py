from sensor.SensorCategory import SensorCategory
from sensor.vSensor import vSensor


class Track(vSensor):
    def __init__(self, name):
        super().__init__(SensorCategory.Track, name)

    def _doWorkDataInput(self, inputdata=None):
        print("doWork Track")

    def addSimData(self, data):
        pass