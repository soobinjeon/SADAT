import math
import json
import time
from multiprocessing import Manager, Process

#for rpLidar
from SimLog import SimLog


class LogSimDispatcher():
    def __init__(self, log, opensrc=""):
        self.Log = log
        self.opensrc = opensrc
        self._rawdata = None
        print("LogSimDispatcher Init")

    def dispatch(self):
        print("Dispatch")
        time.sleep(4)
        self.Log.initLog()
        self._rawdata = self.loadData()
        self.logDispatch(self._rawdata)
        print("end Process")

    def loadData(self):
        print("lodata method called")
        if self.opensrc == "":
            self.opensrc = "../Data/data_2.json"

        with open(self.opensrc, "r") as st_json:
            print("Load log Data..")
            ldata = json.load(st_json)
            return ldata

    def logDispatch(self, rawdata):
        logcnt = 0
        hasStartFlag = False
        datalen = len(rawdata['rawdata'])

        while logcnt < datalen:
            data = rawdata['rawdata'][logcnt]
            start_flag = data['start_flag']

            if hasStartFlag == False and start_flag == True:
                #print("sflag",logcnt,end=", ")
                tempX = []
                tempY = []
                tempXY = []
                innerSflag = False
                innercnt = 0
                while not innerSflag and logcnt < datalen:
                    data = rawdata['rawdata'][logcnt]
                    if innercnt != 0:
                        innerSflag = data['start_flag']

                    distance = data['distance']
                    angle = data['angle']
                    timestamp = data['timestamp']
                    tx, ty = self.getCoordinatebyLidar(distance=distance, angle=angle)
                    tempX.append(tx)
                    tempY.append(ty)

                    innercnt += 1
                    logcnt += 1

                #insert XY coord
                tempXY.append(tempX)
                tempXY.append(tempY)

                #insert XY into shared log
                self.Log.enQueueData(tempXY)
                print(self.Log.getQueueData().qsize())
                #print(self.Log.getQueueData())
                #print(innercnt)
            else:
                logcnt += 1

    def getCoordinatebyLidar(self, distance, angle):
        x = distance * math.cos(math.radians(90 - angle))
        y = -1 * (distance * math.sin(math.radians(90 - angle)))

        return x, y

# if __name__ == '__main__':
#     manager = Manager()
#     simlog = SimLog(manager)
#     gm = LogSimDispatcher(simlog)
#     gm.dispatch()