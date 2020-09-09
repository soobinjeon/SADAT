from Grabber import Grabber
from LogPlayDispatcher import LogPlayDispatcher
from Logger import Logger
from simMode import Mode


class ModeLog(Mode):
    def __init__(self, log, simlog):
        super().__init__(log)
        self.grabber = Grabber(self.log, 1000)
        self.logger = Logger(self.log, simlog)
        self.dispatcher = LogPlayDispatcher(simlog)

    def makeProcess(self):
        self.addProcess("Grabber", self.grabber.startGrab, None)
        self.addProcess("Logger", self.logger.LogWorker, None)
        self.addProcess("LogDispatcher", self.dispatcher.dispatch, None)