from LogSimDispatcher import LogSimDispatcher
from simMode import Mode
import time


class ModeSimulation(Mode):
    def __init__(self, srcmgr):
        super().__init__(None)
        self.lSimDispatcher = LogSimDispatcher(srcmgr)

    def makeProcess(self):
        self.addProcess("FileReader", self.lSimDispatcher.dispatch, None)