from multiprocessing import Manager, Process
from Grabber import Grabber
from LidarLog import LidarLog
from Logger import Logger

class ProcessData:
    name = ""
    target = None
    args = None
    def __init__(self, _name, _target, _args):
        self.name = _name
        self.target = _target
        self.args = _args

class GrabManager:
    procdata = []
    processes = []
    logdata = None
    def __init__(self, manager):
        self.log = LidarLog(manager)
        self.grabber = Grabber(self.log, self, 550)
        self.logger = Logger(self.log)
        self.ProcessList()

    def StartManager(self):
        #set Processes
        for proc in self.procdata:
            self.addProcess(proc)

        for p in self.processes:
            p.start()
            print("Start", p, p.is_alive())

        for p in self.processes:
            p.join()

        print("end Process")

    def ProcessList(self):
        #add grabber
        self.procdata.append(ProcessData("Grabber", self.grabber.startGrab, None))
        #add Logger
        self.procdata.append(ProcessData("Logger", self.logger.LogWorker, None))

    def addProcess(self, procdata):
        if procdata.args is None:
            self.processes.append(Process(name=procdata.name, target=procdata.target))
        else:
            self.processes.append(Process(name=procdata.name, target=procdata.target, args=procdata.args))

    def getNumofProc(self):
        return len(self.processes)

if __name__ == '__main__':
    gm = GrabManager(Manager())
    gm.StartManager()
