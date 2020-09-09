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

        self.testrawdata = []

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
        prevt = 0
        total = 0
        for dataset in iter(logplaydata.get, 'interrupt'):
            print('datalen - ',len(dataset))
            for data in dataset:
                start_flag = data['start_flag']
                timestamp = data['timestamp']

                if start_flag is True:
                    tgap = timestamp - prevt
                    prevt = timestamp
                    total += scan_cnt
                    #print('scntbyCycle-', scan_cnt, total, tgap)
                    if len(tempX) > 0:

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
                    #pass
                    self.inputdata(data, tempX, tempY)
                scan_cnt += 1

                tempdata = str(scan_cnt)+','+str(data['start_flag'])+','+str(data['angle'])+','+str(data['distance'])
                self.testrawdata.append(tempdata)

        # for test
        # with open('../../LogPlayDisrawdata.json', 'w') as outfile:
        #     print('Raw data writing')
        #     #json.dump(self.testrawdata, outfile)
        #     for d in self.testrawdata:
        #         outfile.write(d+'\n')
        #     print("Raw data Write Complete")
        #self.Log.enQueueData(self.getEOFMessage())

# if __name__ == '__main__':
#     manager = Manager()
#     simlog = SimLog(manager)
#     gm = LogSimDispatcher(simlog)
#     gm.dispatch()