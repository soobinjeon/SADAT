import time
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal

class playbackInfo():

    def __init__(self):
        self.mode = 0
        self.maxLength = 0
        self.currentIdx = 0

class taskLoopPlay(QThread):
    signal = pyqtSignal([playbackInfo])

    def __init__(self, parent=None, simlog=None, manager=None):
        super(taskLoopPlay, self).__init__(parent=parent)
        self.task = manager.Queue()
        self.simlog = simlog
        self.originData = []

        self.pbInfo = playbackInfo()
        self.playidx = 0
        self.isPause = False
        self.initPlay()

        self.value = 0
        self.vel = None

    def initPlay(self):
        self.playidx = 0
        self.isPause = False

    def setValue(self, value):
        self.value = value

    def setVelocity(self, vel):
        self.vel = vel

    def setSimMode(self):
        self.task.put(1)


    def setLoggingMode(self):
        self.task.put(0)

    def setPlayMode(self):
        self.initPlay()
        self.task.put(2)

    def setPause(self):
        if not self.isPause:
            self.isPause = True
        else:
            self.isPause = False
            self.task.put(2)

    def stop(self):
        self.task.put('stop')
        self.simlog.enQueueData('interrupt')

    def run(self):
        for td in iter(self.task.get, 'stop'):
            #pass
            if td == 0:
                lq = self.simlog.getQueueData()
                print("store origin data")
                for data in iter(lq.get, 'interrupt'):
                    self.simlog.enQueuePlayData(data)

            #Sim Mode
            if td == 1:
                lq = self.simlog.getQueueData()
                print("store origin data")
                for data in iter(lq.get, 'interrupt'):
                    self.originData.append(data)
                    #time.sleep(1 / self.vel)
                self.pbInfo.maxLength = len(self.originData)
                self.signal.emit(self.pbInfo)
                print("Store Completed")

            elif td == 2:
                print("play data")
                self.pbInfo.mode = 1
                self.playidx
                while self.playidx < self.pbInfo.maxLength:
                    if self.isPause:
                        break
                    self.pbInfo.currentIdx = self.playidx
                    #data.append(self.pbInfo)
                    self.simlog.enQueuePlayData(self.originData[self.playidx])
                    self.signal.emit(self.pbInfo)
                    time.sleep(1 / self.vel)
                    self.playidx += 1
                # for idx, data in enumerate(self.originData):
                #     self.pbInfo.currentIdx = idx
                #     data.append(self.pbInfo)
                #     self.simlog.enQueuePlayData(data)
                #     time.sleep(1 / self.vel)