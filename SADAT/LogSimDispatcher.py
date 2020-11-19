import math
import json
import time

from Dispatcher import Dispatcher
from log.makeRPLidarLog import makeRPLidarLog


class LogSimDispatcher(Dispatcher):

    def __init__(self, log, opensrc=""):
        super().__init__()
        self.Log = log
        self.opensrc = opensrc
        self._rawdata = None
        print("LogSimDispatcher Init")
        print(self.guiApp)

    def dispatch(self):
        time.sleep(1)
        self.Log.initLog()
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
        tempX = []
        tempY = []
        tempXY = []
        cnt = 0
        #print(len(rawdata))
        for rdata in rawdata:
            tempXY = []
            tempX = []
            tempY = []

            tempX, tempY = self.inputdataArray(rdata)
            tempXY.append(tempX)
            tempXY.append(tempY)
            tempXY.append(rdata.timestamp[0])
            tempXY.append(rdata.start_flag[0])
            self.Log.enQueueData(tempXY)
            if cnt % 100 == 0:
                print(cnt)
            cnt += 1

        print("End Read Data")
        self.Log.enQueueData(self.getEOFMessage())

    def logDispatch_old(self, rawdata):
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
                timestamp = 0
                sflag = False
                while not innerSflag and logcnt < datalen:
                    data = rawdata['rawdata'][logcnt]
                    if innercnt != 0:
                        innerSflag = data['start_flag']

                    distance = data['distance']
                    angle = data['angle']
                    timestamp = data['timestamp']
                    sflag = data['start_flag']
                    tx, ty = self.getCoordinatebyLidar(distance=distance, angle=angle)
                    tempX.append(tx)
                    tempY.append(ty)


                    innercnt += 1
                    logcnt += 1

                #insert XY coord
                tempXY.append(tempX)
                tempXY.append(tempY)
                tempXY.append(timestamp)
                tempXY.append(sflag)

                #insert XY into shared log
                self.Log.enQueueData(tempXY)
                #print(self.Log.getQueueData().qsize(), tempXY[0][0], tempXY[1][0])
                #self.signal.emit(tempXY)
                #print(self.Log.getQueueData())
                #print(innercnt)
            else:
                logcnt += 1

        self.Log.enQueueData(self.getEOFMessage())

# if __name__ == '__main__':
#     manager = Manager()
#     simlog = SimLog(manager)
#     gm = LogSimDispatcher(simlog)
#     gm.dispatch()