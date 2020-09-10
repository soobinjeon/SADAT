import platform
import time
import datetime as pydatetime
from LidarLog import LidarLog
from multiprocessing import Manager
from library.pyrplidar.pyrplidar import PyRPlidar


def get_now():
    return pydatetime.datetime.now()

def get_now_timestamp():
    return get_now().timestamp()


class Grabber:

    def __init__(self, _log, motorpwm):
        self.log = _log
        self.log.initLog(motorpwm)
        self.pwm = motorpwm
        self.lidar = None

    def connect(self):
        try:
            self.lidar = PyRPlidar()
            if platform.system() == 'Windows':
                self.lidar.connect(port="COM4", baudrate=256000, timeout=3, isWindows=True)
            else:
                self.lidar.connect(port="/dev/ttyUSB0", baudrate=256000, timeout=3)
            #Windows

            # Linux   : "/dev/ttyUSB0"
            # MacOS   : "/dev/cu.SLAB_USBtoUART"
            # Windows : "COM5"
            # print("info")
            # print(self.lidar.get_info())
            # print("health")
            # print(self.lidar.get_health())
            # print("samplerate")
            # print(self.lidar.get_samplerate())
            print("mode")
            print(self.lidar.get_scan_mode_count())
            print("typical")
            print(self.lidar.get_scan_mode_typical())
            print("scan mode")
            print(self.lidar.get_scan_modes())

            # scan_modes = self.lidar.get_scan_modes()
            # print("scan modes :")
            # for scan_mode in scan_modes:
            #     print(scan_mode)

        except Exception as e:
            print("Exception",e)
            self.disconnect()

    def startGrab(self):
        self.log.initLog(self.pwm)
        if self.log is not None:
            self.connect()
            self.startLidar()
            self.disconnect()

    def startLidar(self):
        try:
            self.lidar.set_motor_pwm(self.pwm)
            time.sleep(0.5)
            print("start grab")
            scan_generator = self.lidar.start_scan_express(3)
            ptime = int(get_now_timestamp())
            print("%d"%ptime)

            prevtime = 0
            c_cnt = 0
            startcnt = 0
            dataset = []
            for count, scan in enumerate(scan_generator()):

                #self.log.enQueueData(scan, get_now_timestamp())
                dataset.append(self.log.makeData(scan, get_now_timestamp()))
                ctime = int(get_now_timestamp())
                tgap = ctime - ptime

                #Send Data after 1 cycle
                if scan.start_flag:
                    startcnt += 1
                    self.log.enQueueDataNew(dataset)
                    dataset = []

                if tgap > prevtime:
                    print("Time : ",tgap,count,(count-c_cnt),startcnt)
                    c_cnt = count
                    startcnt = 0

                if tgap == 120:
                    self.log.enQueueData('interrupt', get_now_timestamp())
                    break

                prevtime = tgap

                # print(count, scan)
                # if cnt == 100: break
        except Exception as e:
            print("Exception",e)
        finally:
            self.lidar.stop()
            self.lidar.set_motor_pwm(0)

    def disconnect(self):
        self.lidar.disconnect()


if __name__ == '__main__':
    llog = LidarLog(Manager())
    grab = Grabber(llog, 550)
    grab.startGrab()
