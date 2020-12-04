import math
import json
import time

from Dispatcher import Dispatcher
from log.makeRPLidarLog import makeRPLidarLog
from sensor.SenAdptMgr import AttachedSensorName
from sensor.SensorCategory import SensorCategory
from sensor.vsensor.RPLidar2Dv import RPLidar2Dv


class LogSimDispatcher(Dispatcher):

    def __init__(self, srcmgr, opensrc=""):
        super().__init__()
        self.sourcemanager = srcmgr
        self.opensrc = opensrc
        print("LogSimDispatcher Init")
        print(self.guiApp)

    def dispatch(self):
        self.loadData()
        self.logDispatch()
        print("end Process")

    def loadData(self):
        print("lodata method called")
        if self.opensrc == "":
            self.opensrc = "../../Data/data_1.dat"

        #파일을 저장할 때 head 부분에 디바이스 네임을 작성해줘야함
        #헤더파일의 디바이스 네임에 따라 rawdata에 저장될 수 있도록 변경해야함
        lidarlog = makeRPLidarLog(self.opensrc);
        self._rawdata[AttachedSensorName.RPLidar2DVirtual] = lidarlog.fromlogFile()

    def logDispatch(self):
        for scate in self._rawdata.keys():
            if scate in self.sourcemanager.AllSensors.keys():
                val = self._rawdata[scate]
                sensor = self.sourcemanager.AllSensors[scate]
                sensor.doWork(val)