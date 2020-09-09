import time
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal

class playbackInfo():

    def __init__(self):
        self.mode = 0
        self.maxLength = 0
        self.currentIdx = 0
        self.setfps = 0

class taskLoopPlay(QThread):
    signal = pyqtSignal([playbackInfo])
    PLAYMODE_LOGPLAY = 0
    PLAYMODE_LOAD = 1
    PLAYMODE_PLAY = 2
    PLAYMODE_PAUSE = 3
    PLAYMODE_SETVALUE = 4

    def __init__(self, parent=None, simlog=None, manager=None):
        super(taskLoopPlay, self).__init__(parent=parent)
        self.guiApp = parent
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
        self.task.put(self.PLAYMODE_LOAD)


    def setLoggingMode(self):
        self.task.put(self.PLAYMODE_LOGPLAY)

    def setPlayMode(self):
        self.initPlay()
        self.task.put(self.PLAYMODE_PLAY)

    def setPause(self, isResume):
        if not isResume:
            self.isPause = True
        else:
            self.isPause = False
            self.task.put(self.PLAYMODE_PLAY)

    def setPlayPoint(self, value):
        if not self.isPause:
            self.isPause = True

        self.playidx = value
        self.task.put(self.PLAYMODE_SETVALUE)

    def stop(self):
        self.task.put('stop')
        self.simlog.enQueueData('interrupt')

    def run(self):
        for td in iter(self.task.get, 'stop'):
            #pass
            if td == self.PLAYMODE_LOGPLAY:
                lq = self.simlog.getQueueData()
                print("store origin data")
                for data in iter(lq.get, 'interrupt'):
                    self.simlog.enQueuePlayData(data)


            #Sim Mode
            if td == self.PLAYMODE_LOAD: #Load Data
                lq = self.simlog.getQueueData()
                self.guiApp.setStatus("Loading origin data")
                print("store origin data")
                tcnt = 0
                prevtime = 0
                fps = 0
                fpscnt = 0
                for data in iter(lq.get, 'interrupt'):
                    self.originData.append(data)
                    tcnt += 1
                    if prevtime < int(data[2]):
                        print("frame per sec :",tcnt)
                        fps += tcnt
                        fpscnt += 1
                        tcnt = 0

                    prevtime = int(data[2])
                    #print(data[2], data[3])
                    #time.sleep(1 / self.vel)

                #calculate frame per sec
                fps = 0 if fpscnt == 0 else int(fps / fpscnt)

                self.pbInfo.mode = self.PLAYMODE_LOAD
                self.pbInfo.maxLength = len(self.originData)
                self.pbInfo.setfps = fps
                self.signal.emit(self.pbInfo)
                self.guiApp.setStatus("Log data Load Completed")
                self.simlog.enQueuePlayData(self.originData[self.playidx])

            elif td == self.PLAYMODE_PLAY:
                self.pbInfo.mode = self.PLAYMODE_PLAY
                while self.playidx < self.pbInfo.maxLength:
                    if self.isPause:
                        break
                    self.pbInfo.currentIdx = self.playidx
                    #data.append(self.pbInfo)
                    self.simlog.enQueuePlayData(self.originData[self.playidx])
                    self.signal.emit(self.pbInfo)
                    time.sleep(1 / self.vel)
                    self.playidx += 1

            elif td == self.PLAYMODE_SETVALUE:
                self.pbInfo.mode = self.PLAYMODE_SETVALUE
                self.pbInfo.currentIdx = self.playidx
                self.simlog.enQueuePlayData(self.originData[self.playidx])
                self.signal.emit(self.pbInfo)
                # for idx, data in enumerate(self.originData):
                #     self.pbInfo.currentIdx = idx
                #     data.append(self.pbInfo)
                #     self.simlog.enQueuePlayData(data)
                #     time.sleep(1 / self.vel)