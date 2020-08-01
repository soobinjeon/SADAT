from pyrplidar import PyRPlidar
import time
import datetime as pydatetime


def get_now():
    return pydatetime.datetime.now()

def get_now_timestamp():
    return get_now().timestamp()


class Grabber:
    lidar = None

    def __init__(self, _log, motorpwm):
        self.log = _log
        self.log.initLog(motorpwm)
        self.pwm = motorpwm

    def connect(self):
        try:
            self.lidar = PyRPlidar()
            self.lidar.connect(port="/dev/ttyUSB0", baudrate=256000, timeout=3)
            # Linux   : "/dev/ttyUSB0"
            # MacOS   : "/dev/cu.SLAB_USBtoUART"
            # Windows : "COM5"
            # print("info")
            # print(self.lidar.get_info())
            # print("health")
            # print(self.lidar.get_health())
            # print("samplerate")
            # print(self.lidar.get_samplerate())
            # print("mode")
            # print(self.lidar.get_scan_mode_count())
            # print("typical")
            # print(self.lidar.get_scan_mode_typical())
            # print("scan mode")
            # print(self.lidar.get_scan_modes())

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
            time.sleep(1)

            scan_generator = self.lidar.force_scan()
            ptime = int(get_now_timestamp())
            print("%d"%ptime)

            prevtime = 0
            for count, scan in enumerate(scan_generator()):
                self.log.enQueueData(scan, get_now_timestamp())
                ctime = int(get_now_timestamp())
                tgap = ctime - ptime

                if tgap > prevtime:
                    print("Time : ",tgap)

                if tgap == 60:
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