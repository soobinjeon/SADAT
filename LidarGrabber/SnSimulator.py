import sys
from multiprocessing import Manager, Process
from PyQt5.QtWidgets import QApplication
from LidarLog import LidarLog
from ModeLog import ModeLog
from ModeSimulation import ModeSimulation
from SimLog import SimLog
from gui.guiMain import GUI_CONTROLLER
from simMode import Mode
import time

from taskLoopPlay import taskLoopPlay
from taskPlanview import taskPlanview


class SnSimulator:
    processes = []

    def __init__(self, manager, gapp=None):
        self.guiApp = gapp
        self.manager = manager
        self.rawlog = LidarLog(manager)
        self.simlog = SimLog(manager)
        self.procs = {}
        self.pvthread = None
        self.lpthread = None

        self.Velocity = 0

        self.plugins = None

        self.loadPlugin()
        self.defineProcess()

    def StartManager(self):
        # self.CommandMode()
        print("exit")
        for p in self.processes:
            p.join()

        print("end Process")

    def setAction(self, mode):

        if mode is Mode.MODE_SIM:
            self.lpthread.setSimMode()
        elif mode is Mode.MODE_LOG:
            self.lpthread.setLoggingMode()

        self.cleanProcess()
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

    def cleanProcess(self):
        if len(self.processes) != 0:
            #clean process start
            print("Wait process finishing for cleaning process list")
            for p in self.processes:
                p.join()

            self.processes.clear()
            print("Clean, process length :", len(self.processes))

    def defineProcess(self):
        # init planview thread
        self.pvthread = taskPlanview(self.guiApp, self.simlog)
        self.pvthread.signal.connect(self.guiApp.changePosition)
        self.pvthread.start()

        self.lpthread = taskLoopPlay(self.guiApp, self.simlog, self.manager)
        self.lpthread.signal.connect(self.guiApp.playbackstatus)
        self.lpthread.setVelocity(60)
        self.lpthread.start()

        # init log process
        self.procs[Mode.MODE_LOG] = ModeLog(self.rawlog)
        self.procs[Mode.MODE_SIM] = ModeSimulation(self.simlog)
        print(self.procs)

    def addProcess(self, procdata):
        if procdata.args is None:
            self.processes.append(Process(name=procdata.name, target=procdata.target))
        else:
            self.processes.append(Process(name=procdata.name, target=procdata.target, args=procdata.args))

    def getNumofProc(self):
        return len(self.processes)

    def loadPlugin(self):
        self.plugins = []
        #self.plugins.append(Plugin())
        #플러그인 상속받은 Tracker Algorithm 생성

    def setVelocity(self, vel):
        v = int(vel)
        self.lpthread.setVelocity(v)
        self.Velocity = v

    def getVelocity(self):
        return self.Velocity

    def playMode(self):
        self.lpthread.setPlayMode()
        self.guiApp.gcontrol.setPlayMode(GUI_CONTROLLER.PLAYMODE)

    def PauseMode(self):
        self.lpthread.setPause(False)
        self.guiApp.gcontrol.setPlayMode(GUI_CONTROLLER.RESUMEMODE)

    def ResumeMode(self):
        self.lpthread.setPause(True)
        self.guiApp.gcontrol.setPlayMode(GUI_CONTROLLER.PLAYMODE)


if __name__ == '__main__':
    gm = SnSimulator(Manager())
    gm.StartManager()
