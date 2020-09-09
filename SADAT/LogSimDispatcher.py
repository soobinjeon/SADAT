import math
import json
import time

from Dispatcher import Dispatcher


class LogSimDispatcher(Dispatcher):

    def __init__(self, log, opensrc=""):
        super().__init__()
        self.Log = log
        self.opensrc = opensrc
        self._rawdata = None
        print("LogSimDispatcher Init")
        print(self.guiApp)

    def dispatch(self):
        print("Dispatch")
        time.sleep(1)
        self.Log.initLog()
        self._rawdata = self.loadData()
        self.logDispatch(self._rawdata)
        print("end Process")

    def loadData(self):
        print("lodata method called")
        if self.opensrc == "":
            self.opensrc = "../../Data/data_1.json"

        with open(self.opensrc, "r") as st_json:
            print("Load log Data..")
            ldata = json.load(st_json)
            return ldata

    def logDispatch(self, rawdata):
        logcnt = 0
        hasStartFlag = False

        tempX = []
        tempY = []
        tempXY = []
        timestamp = 0
        scan_cnt = 0
        datalen = len(rawdata['rawdata'])

        for rdata in rawdata['rawdata']:

            for data in rdata:
                start_flag = data['start_flag']
                timestamp = data['timestamp']

                if start_flag is True:
                    if len(tempX) > 0:
                        # insert XY coord
                        tempXY.append(tempX)
                        tempXY.append(tempY)
                        tempXY.append(timestamp)
                        tempXY.append(start_flag)

                        # insert XY into shared log
                        self.Log.enQueueData(tempXY)

                    scan_cnt = 0
                    tempX = []
                    tempY = []
                    tempXY = []
                    self.inputdata(data, tempX, tempY)

                else:
                    # pass
                    self.inputdata(data, tempX, tempY)

                logcnt += 1
                scan_cnt += 1

        self.Log.enQueueData(self.getEOFMessage())

    def inputdata(self, data, tempx, tempy):
        distance = data['distance']
        angle = data['angle']
        sflag = data['start_flag']
        tx, ty = self.getCoordinatebyLidar(distance=distance, angle=angle)
        tempx.append(tx)
        tempy.append(ty)

    def getCoordinatebyLidar(self, distance, angle):
        x = distance * math.cos(math.radians(90 - angle))
        y = -1 * (distance * math.sin(math.radians(90 - angle)))

        return x, y

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