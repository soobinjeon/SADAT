from abc import *
from SimProcess import SimProcess


class Mode(metaclass=ABCMeta):
    MODE_LOG = 1
    MODE_SIM = 2

    def __init__(self, log):
        self.log = log
        self.procList = []
        self.lSimDispatcher = None

    def addProcess(self, name, func, args):
        self.procList.append(SimProcess(name=name, target=func, args=args))

    def getProcesses(self):
        if len(self.procList) == 0:
            self.makeProcess()
        return self.procList

    def setVelocity(self, vel):
        if self.lSimDispatcher is not None:
            self.lSimDispatcher.setVelocity(vel)


    @abstractmethod
    def makeProcess(self):
        pass
