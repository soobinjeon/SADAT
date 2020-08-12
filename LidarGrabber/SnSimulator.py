import sys
from multiprocessing import Manager, Process
from PyQt5.QtWidgets import QApplication
from LidarLog import LidarLog
from ModeLog import ModeLog
from ModeSimulation import ModeSimulation
from SimLog import SimLog
from simMode import Mode
import time

class SnSimulator:
    processes = []

    def __init__(self, manager):
        self.rawlog = LidarLog(manager)
        self.simlog = SimLog(manager)
        self.procs = {}
        self.defineProcess()

    def StartManager(self):
        #self.CommandMode()
        print("exit")
        for p in self.processes:
            p.join()

        print("end Process")

    def setMode(self, mode):
        proc = self.procs[mode]
        if proc is not None:
            # set Processes
            for pr in proc.getProcesses():
                self.addProcess(pr)
            for p in self.processes:
                p.start()
                print("Start", p, p.is_alive())

            # for data in iter(self.simlog.getQueueData().get, 'interrupt'):
            #     time.sleep(0.01)

    def defineProcess(self):
        self.procs[Mode.MODE_LOG] = ModeLog(self.rawlog)
        self.procs[Mode.MODE_SIM] = ModeSimulation(self.simlog)

    def addProcess(self, procdata):
        if procdata.args is None:
            self.processes.append(Process(name=procdata.name, target=procdata.target))
        else:
            self.processes.append(Process(name=procdata.name, target=procdata.target, args=procdata.args))

    def getNumofProc(self):
        return len(self.processes)

    def CommandMode(self):
        while True:
            comm = int(input("Input Command(1:sim 2:log 3:exit) : "))

            if comm == 1:
                self.setMode(Mode.MODE_SIM)
            elif comm == 2:
                self.setMode(Mode.MODE_LOG)
            else:
                break
            time.sleep(2)

if __name__ == '__main__':
    gm = SnSimulator(Manager())
    gm.StartManager()
