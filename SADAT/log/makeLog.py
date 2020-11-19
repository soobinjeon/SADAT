from abc import *

class makeLog(metaclass=ABCMeta):
    def __init__(self, filename=None):
        self.filename=None
        self.lf = None
        if filename != None:
            self.filename = filename

    def setFileName(self, filename):
        self.filename = filename

    def startLog(self):
        self.lf = open(self.filename, 'wb')
        print("Log Started")

    def stopLog(self):
        self.lf.close()

    @abstractmethod
    def logData(self, loggingdata=None):
        pass

    @abstractmethod
    def fromlogFile(self):
        pass