import time

class SimLog:
    LOGPLAY_MODE_SIM = 0
    LOGPLAY_MODE_SAVE = 1

    def __init__(self, manager):
        print("Sim Log Init")
        self.logginData = manager.Queue()
        self.simLogData = manager.Queue()
        self.playData = manager.Queue()

        self.mode = self.LOGPLAY_MODE_SIM

    def initLog(self):

        if not self.simLogData.empty():
            while not self.simLogData.empty():
                self.simLogData.get()

    def enQueueData(self, data):
        qsize = self.simLogData.qsize()
        # while qsize > 1000:
        #     time.sleep(0.001)
        #     qsize = self.simLogData.qsize()

        self.simLogData.put(data)

    def getQueueData(self):
        return self.simLogData

    def enQueuePlayData(self, data):
        self.playData.put(data)

    def getQueuePlayData(self):
        return self.playData

    def enQueueLoggingData(self, data):
        self.logginData.put(data)

    def getQueueLoggingData(self):
        return self.logginData

    def disconnectAllData(self):
        self.enQueueData('interrupt')
        self.enQueueLoggingData('interrupt')
        self.enQueuePlayData('interrupt')

    def setLogPlayMode(self, mode):
        self.mode = mode

    def isLogPlayMode(self):
        return self.mode is self.LOGPLAY_MODE_SIM

    def isLoggingMode(self):
        return self.mode is self.LOGPLAY_MODE_SAVE
