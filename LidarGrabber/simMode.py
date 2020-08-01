from abc import *
from SimProcess import SimProcess


class Mode(metaclass=ABCMeta):
    MODE_LOG = 1
    MODE_SIM = 2

    def __init__(self, log):
        self.log = log
        self.procList = []

    def addProcess(self, name, func, args):
        self.procList.append(SimProcess(name=name, target=func, args=args))

    def getProcesses(self):
        self.makeProcess()
        return self.procList

    @abstractmethod
    def makeProcess(self):
        pass
