from sensor.SensorCategory import SensorCategory
from sensor.vSensor import vSensor


class RPLidar2Dv(vSensor):
    def __init__(self, name):
        super().__init__(SensorCategory.RPLidar2D, name)

    def _doWorkDataInput(self, inputdata=None):
        tempX = []
        tempY = []
        tempXY = []
        # cnt = 0
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
            self._addSimData(tempXY)
            #self.Log.enQueueData(tempXY)
            # if cnt % 100 == 0:
            #     print(cnt)
            # cnt += 1

        # print("End Read Data")
        #self.addData(self.INTERRUPT_MSG)
