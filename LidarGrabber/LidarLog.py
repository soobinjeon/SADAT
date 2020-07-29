from multiprocessing import Manager


class LidarLog:
    motorpwm = 0

    def __init__(self, manager):
        print("Log Init")
        self.lidarDataQueue = manager.Queue()

    def initLog(self, motorpwm):
        self.motorpwm = motorpwm

        if not self.lidarDataQueue.empty():
            while not self.lidarDataQueue.empty():
                self.lidarDataQueue.get()

    def enQueueData(self, scandata, timestamp):
        if scandata == 'interrupt':
            self.lidarDataQueue.put(scandata)
        else:
            data = {}
            data['start_flag'] = scandata.start_flag
            data['quality'] = scandata.quality
            data['angle'] = scandata.angle
            data['distance'] = scandata.distance
            data['timestamp'] = timestamp
            #print(data)
            self.lidarDataQueue.put(data)

    def getQueueData(self):
        return self.lidarDataQueue

