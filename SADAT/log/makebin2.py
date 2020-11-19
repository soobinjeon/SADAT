import numpy as np
import json
import math
from numpy import fromfile

from log.makeRPLidarLog import makeRPLidarLog, RPLidarLogType


def inputdata(data, dis, ang):
    distance = data['distance']
    angle = data['angle']
    sflag = data['start_flag']
    #tx, ty = getCoordinatebyLidar(distance=distance, angle=angle)
    dis.append(distance)
    ang.append(angle)


def getCoordinatebyLidar(distance, angle):
    x = distance * math.cos(math.radians(90 - angle))
    y = -1 * (distance * math.sin(math.radians(90 - angle)))

    return x, y

def loadData():
    print("lodata method called")
    opensrc = "../../Data/data_1.json"

    with open(opensrc, "r") as st_json:
        print("Load log Data..")
        ldata = json.load(st_json)
        return ldata

def runConvert():
    rplidarlog = makeRPLidarLog("data1.dat")
    rplidarlog.startLog()

    rawdata = loadData()

    datalen = len(rawdata['rawdata'])
    print(datalen)

    fulldata = []

    logcnt = 0
    hasStartFlag = False

    dis = []
    ang = []
    ldata = RPLidarLogType()
    timestamp = 0
    scan_cnt = 0
    datalen = len(rawdata['rawdata'])

    for rdata in rawdata['rawdata']:

        for data in rdata:
            start_flag = data['start_flag']
            timestamp = data['timestamp']

            if start_flag is True:
                if len(dis) > 0:
                    # insert XY coord
                    ldata.distance = dis
                    ldata.angle = ang
                    ldata.timestamp = timestamp
                    ldata.start_flag = start_flag

                    # insert XY into shared log
                    rplidarlog.logData(ldata)

                scan_cnt = 0
                dis = []
                ang = []
                ldata = RPLidarLogType()
                inputdata(data, dis, ang)

            else:
                # pass
                inputdata(data, dis, ang)

            logcnt += 1
            scan_cnt += 1

    rplidarlog.stopLog()
    # print(rplidarlog.)
    # print(fulldata[1])
    # print(fulldata[2])
    # cnt = 0
    # with open('data.dat', 'wb') as fp:
    #     for data in fulldata:
    #         np.array([len(data[0])]).tofile(fp, format='<i')
    #         np.array([len(data[1])]).tofile(fp, format='<i')
    #         np.array(data[0], dtype='H').tofile(fp, format='<H')
    #         np.array(data[1], dtype='f').tofile(fp, format='<f')
    #         np.array([data[2]]).tofile(fp, format='<d')
    #         np.array([data[3]]).tofile(fp, format='<?')
    #
    #         if cnt == 0:
    #             print(data[0])
    #             print(data[1])
    #             cnt = 1


runConvert()
cnt = 0
fulldata = []
with open('data.dat', 'rb') as fp:
    while True:
        inputdata = []
        var1 = fromfile(fp, "<i", 2)
        if var1.size < 2:
            break
        var2 = fromfile(fp, "<H", var1[0])
        var3 = fromfile(fp, "<f", var1[1])
        var4 = fromfile(fp, "<d", 1)
        var5 = fromfile(fp, "<?", 1)

        inputdata.append(var2)
        inputdata.append(var3)
        inputdata.append(var4)
        inputdata.append(var5)
        fulldata.append(inputdata)
        cnt += 1


print(fulldata[0])

cnt = 0
rpmodule = makeRPLidarLog('data1.dat')
fulldata = rpmodule.fromlogFile()
print(fulldata[1].angle)
# print(var1)
# print(var2)
# print(var3)
# print(var4)
# print(var5)
# var1 = 3.32
# var2 = 1.35452
# with open('data.dat', 'wb') as fp:
#     np.array([var1, var2]).tofile(fp, format='d')
#
# with open('data.dat', 'rb') as fp:
#     val1 = fromfile(fp, "d", 2)

# print(val1)