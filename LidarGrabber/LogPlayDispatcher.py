import math
import json
import time
from PyQt5.QtCore import pyqtSignal

from Dispatcher import Dispatcher


class LogPlayDispatcher(Dispatcher):

    def __init__(self, log):
        super().__init__()
        self.Log = log
        self._rawdata = None
        print("LogPlayDispatcher Init")
        print(self.guiApp)

    def dispatch(self):
        time.sleep(1)
        self.logDispatch()


    def logDispatch(self):
        logcnt = 0
        hasStartFlag = False

        tempX = []
        tempY = []
        tempXY = []
        timestamp = 0
        scan_cnt = 0
        logplaydata = self.Log.getQueueLoggingData()
        for data in iter(logplaydata.get, 'interrupt'):
            start_flag = data['start_flag']
            timestamp = data['timestamp']

            if start_flag is True:
                if len(tempX) > 0:
                    #print('scntbyCycle-',scan_cnt)
                    # insert XY coord
                    tempXY.append(tempX)
                    tempXY.append(tempY)
                    tempXY.append(timestamp)
                    tempXY.append(start_flag)

                    # insert XY into shared log
                    self.Log.enQueueData(tempXY)
                    # print(self.Log.getQueueData().qsize(), tempXY[0][0], tempXY[1][0])
                    # self.signal.emit(tempXY)
                    # print(self.Log.getQueueData())
                    # print(innercnt)

                scan_cnt = 0
                tempX = []
                tempY = []
                tempXY = []
                self.inputdata(data, tempX, tempY)

            else:
                self.inputdata(data, tempX, tempY)
            scan_cnt += 1


        #self.Log.enQueueData(self.getEOFMessage())

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

# if __name__ == '__main__':
#     manager = Manager()
#     simlog = SimLog(manager)
#     gm = LogSimDispatcher(simlog)
#     gm.dispatch()