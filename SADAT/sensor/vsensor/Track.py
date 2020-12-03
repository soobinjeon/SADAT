from sensor.SensorCategory import SensorCategory
from sensor.vSensor import vSensor


class Track(vSensor):
    def __init__(self):
        super().__init__(SensorCategory.Track, "Track")