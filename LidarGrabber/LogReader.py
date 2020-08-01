import json
import math


class LogReader:
    def startRead(self, lq):
        print("Start Read")
        x = []
        y = []

        for _ in range(430):
            x.append(0)
            y.append(0)

        with open("/Users/soobinjeon/Developments/AD/LidarTracker/Data/data_2.json", "r") as st_json:
            ldata = json.load(st_json)

            cnt = 0
            prevsf = 0
            startTimestamp = 0

            ischecked = False
            inputdata = []
            for data in ldata['rawdata']:
                if startTimestamp == 0:
                    startTimestamp = data['timestamp']
                ctimestamp = data['timestamp']
                tgap = ctimestamp - startTimestamp

                if tgap > 3.0 and data['start_flag'] == True and cnt != 0:
                    gap = cnt - prevsf
                    prevsf = cnt
                    if ischecked == False:
                        ischecked = True
                    else:
                        ischecked = False

                        cnt = 0
                        xy = []
                        for data in inputdata:
                            x[cnt] = data['distance'] * math.cos(math.radians(90 - data['angle']))
                            y[cnt] = -1 * (data['distance'] * math.sin(math.radians(90 - data['angle'])))
                            # print(x[cnt], y[cnt])
                            cnt += 1

                        xy.append(x)
                        xy.append(y)

                        lq.enQueueData(xy)
                        print(lq)
                        inputdata.clear()
                        # break

                if ischecked:
                    inputdata.append(data)

                cnt += 1

            lq.enQueueData("interrupt")