import json

class Logger:
    def __init__(self, _log, _simlog=None):
        self.log = _log
        self.simlog = _simlog

    def LogWorker(self):
        print("Init Log Worker")
        outdata = {}
        outdata['motorpwm'] = self.log.motorpwm
        outdata['rawdata'] = []
        rawdata = outdata['rawdata']
        dataqueue = self.log.getQueueData()

        if self.simlog.isLogPlayMode():
            print('log play start')
            self.logPlay(dataqueue)
        else:
            print('data write start')
            cnt = 0
            for data in iter(dataqueue.get, 'interrupt'):
                rawdata.append(data)
                cnt += 1
            print('total cnt = ',cnt)
            #print(outdata)
            with open('../../data.json','w') as outfile:
                print('data writing')
                json.dump(outdata, outfile)
                print("data Write Complete")
            print('completed')

    def logPlay(self, dq):
        for data in iter(dq.get, 'interrupt'):
           self.simlog.enQueueLoggingData(data)

        self.simlog.enQueueLoggingData('interrupt')
