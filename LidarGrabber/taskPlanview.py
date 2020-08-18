import time
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal

class taskPlanview(QThread):
    signal = pyqtSignal([list])
    working = True

    def __init__(self, parent=None, simlog=None):
        super(taskPlanview, self).__init__(parent=parent)
        self.simlog = simlog

    def stop(self):
        self.working = False

    def run(self):
        #pass
        lq = self.simlog.getQueuePlayData()
        for data in iter(lq.get, 'interrupt'):
            self.signal.emit(data)