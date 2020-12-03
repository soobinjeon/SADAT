from sensor.SensorCategory import SensorCategory
from sensor.vSensor import vSensor


class RPLidar2Dv(vSensor):
    NAME = "RPLidar2D A3 Virtual"
    def __init__(self):
        super().__init__(SensorCategory.Lidar2D, self.NAME)

    def doWorkDataInput(self, inputdata=None):
        print("doWork RPLidar 2D v")
        tempX = []
        tempY = []
        tempXY = []
        cnt = 0
        # print(len(rawdata))
        for rdata in inputdata:
            tempXY = []
            tempX = []
            tempY = []

            tempX, tempY = self._inputdataArray(rdata)
            tempXY.append(tempX)
            tempXY.append(tempY)
            tempXY.append(rdata.timestamp[0])
            tempXY.append(rdata.start_flag[0])
            self.addData(tempXY)
            #self.Log.enQueueData(tempXY)
            if cnt % 100 == 0:
                print(cnt)
            cnt += 1

        print("End Read Data")
        self.addData(self.INTERRUPT_MSG)
        #self.Log.enQueueData(self.getEOFMessage())