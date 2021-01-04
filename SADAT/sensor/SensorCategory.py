from enum import Enum


class SensorCategory(Enum):
    RPLidar2D = 1
    Lidar2D = 2
    Lidar3D = 3
    Radar = 4
    Camera = 5
    Ultrasonic = 6
    IMU = 7
    ESC = 8

    Track = 11
    Detection = 12