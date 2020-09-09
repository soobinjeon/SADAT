from abc import *


class LogP(metaclass=ABCMeta):

    INTERRUPT_MSG = 'interrupt'
    def __init__(self):
        self.queuelist = []

    def addQueueList(self, queue):
        self.queuelist.append(queue)
        return queue

    def DisconnectLogs(self):
        for q in self.queuelist:
            q.put(self.INTERRUPT_MSG)