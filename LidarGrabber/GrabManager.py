from multiprocessing import Manager, Process
from LidarLog import LidarLog
from ModeLog import ModeLog
from ModeSimulation import ModeSimulation
from simMode import Mode


class GrabManager:
    processes = []

    def __init__(self, manager):
        self.log = LidarLog(manager)
        self.procs = {}
        self.defineProcess()

    def StartManager(self):
        self.CommandMode()

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

    def defineProcess(self):
        self.procs[Mode.MODE_LOG] = ModeLog(self.log)
        self.procs[Mode.MODE_SIM] = ModeSimulation(self.log)

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

if __name__ == '__main__':
    gm = GrabManager(Manager())
    gm.StartManager()
