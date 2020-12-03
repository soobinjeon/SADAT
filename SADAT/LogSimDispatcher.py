import math
import json
import time

from Dispatcher import Dispatcher
from log.makeRPLidarLog import makeRPLidarLog


class LogSimDispatcher(Dispatcher):

    def __init__(self, srcmgr, opensrc=""):
        super().__init__()
        self.sourcemanager = srcmgr
        self.opensrc = opensrc
        self._rawdata = None
        print("LogSimDispatcher Init")
        print(self.guiApp)

    def dispatch(self):
        self._rawdata = self.loadData()
        self.logDispatch(self._rawdata)
        print("end Process")

    def loadData(self):
        print("lodata method called")
        if self.opensrc == "":
            self.opensrc = "../../Data/data_1.dat"

        lidarlog = makeRPLidarLog(self.opensrc);
        return lidarlog.fromlogFile()

    def logDispatch(self, rawdata):
        if "RPLidar2D A3 Virtual" in self.sourcemanager.AllSensors:
            sensor = self.sourcemanager.AllSensors["RPLidar2D A3 Virtual"]
            sensor.doWorkDataInput(rawdata)