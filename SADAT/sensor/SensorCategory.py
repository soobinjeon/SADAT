from enum import Enum


class SensorCategory(Enum):
    Lidar2D = 1
    Lidar3D = 2
    Radar = 3
    Camera = 4
    Ultrasonic = 5
    IMU = 6
    ESC = 7

    Track = 11
    Detection = 12