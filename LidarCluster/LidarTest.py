from pyrplidar import PyRPlidar
import time

lidar = PyRPlidar()
lidar.connect(port="/dev/ttyUSB0", baudrate=256000, timeout=3)
# Linux   : "/dev/ttyUSB0"
# MacOS   : "/dev/cu.SLAB_USBtoUART"
# Windows : "COM5"
try:
    lidar.set_motor_pwm(660)
    time.sleep(2)

    scan_generator = lidar.force_scan()

    cnt = 0
    for count, scan in enumerate(scan_generator()):
        if scan.start_flag == True:
            print(count, scan)
            cnt += 1
        if cnt == 30: break
        #print(count, scan)
        #if cnt == 100: break

except Exception as e:
    print("Exception",e)
finally:
    lidar.stop()
    lidar.set_motor_pwm(0)
    lidar.disconnect()