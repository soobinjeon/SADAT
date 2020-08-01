from Grabber import Grabber
from Logger import Logger
from simMode import Mode


class ModeLog(Mode):
    def __init__(self, log):
        super().__init__(log)
        self.grabber = Grabber(self.log, 550)
        self.logger = Logger(self.log)

    def makeProcess(self):
        self.addProcess("Grabber", self.grabber.startGrab, None)
        self.addProcess("Logger", self.logger.LogWorker, None)