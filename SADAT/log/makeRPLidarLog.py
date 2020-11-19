import numpy as np
from log.makeLog import makeLog
from numpy import fromfile

class RPLidarLogType():
    # data['start_flag']
    # data['quality']
    # data['angle']
    # data['distance']
    # data['timestamp']
    _DISTANCE = 'distance'
    _ANGLE = 'angle'
    _TIMESTAMP = 'timestamp'
    _QUILITY = 'quility'
    _STARTFLAG = 'start_flag'

    def __init__(self):
        self.start_flag = []
        self.angle = []
        self.distance = []
        self.timestamp = []
        self.quility = []

        # self.lidardata = {self._STARTFLAG: self.start_flag,
        #                   self._ANGLE: self.angle,
        #                   self._DISTANCE: self.distance,
        #                   self._TIMESTAMP: self.timestamp,
        #                   self._QUILITY: self.quility}

    # def addData(self, key, value):
    #     self.lidardata[key].append(value)
    #
    # def getData(self, key):
    #     return self.lidardata[key][0]



class makeRPLidarLog(makeLog):
    def __init__(self, filename):
        super().__init__(filename)
        self.fullLogData = []

    def logData(self, loggingdata=None):
        self.fullLogData.append(loggingdata)

        np.array([len(loggingdata.distance), len(loggingdata.angle)]).tofile(self.lf, format='<i')
        np.array(loggingdata.distance, dtype='H').tofile(self.lf, format='<H')
        np.array(loggingdata.angle, dtype='f').tofile(self.lf, format='<f')
        np.array([loggingdata.timestamp]).tofile(self.lf, format='<d')
        np.array([loggingdata.start_flag]).tofile(self.lf, format='<?')

    def fromlogFile(self):
        self.fullLogData.clear()

        with open(self.filename, 'rb') as fp:
            while True:
                rpdata = RPLidarLogType()
                dsize = fromfile(fp, "<i", 2)
                if dsize.size < 2:
                    break
                rpdata.distance = fromfile(fp, "<H", dsize[0])
                rpdata.angle = fromfile(fp, "<f", dsize[1])
                rpdata.timestamp = fromfile(fp, "<d", 1)
                rpdata.start_flag = fromfile(fp, "<?", 1)

                self.fullLogData.append(rpdata)

        return self.fullLogData