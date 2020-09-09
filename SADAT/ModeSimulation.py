from LogSimDispatcher import LogSimDispatcher
from simMode import Mode
import time


class ModeSimulation(Mode):
    def __init__(self, log):
        super().__init__(log)
        self.lSimDispatcher = LogSimDispatcher(log)

    def makeProcess(self):
        self.addProcess("FileReader", self.lSimDispatcher.dispatch, None)