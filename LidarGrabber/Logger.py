import json

class Logger:
    def __init__(self, _log):
        self.log = _log
        print("test")

    def LogWorker(self):
        print("Init Log Worker")
        outdata = {}
        outdata['motorpwm'] = self.log.motorpwm
        outdata['rawdata'] = []
        rawdata = outdata['rawdata']
        dataqueue = self.log.getQueueData()
        cnt = 0
        for data in iter(dataqueue.get, 'interrupt'):
            rawdata.append(data)
            cnt += 1

        #print(outdata)
        with open('../../data.json','w') as outfile:
            json.dump(outdata, outfile)
            #print("data Write Complete")
