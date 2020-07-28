import json
import matplotlib.pyplot as plt
import math
from celluloid import Camera
import time
import threading

def draw(x, y):
    global is_plot
    while is_plot:
        plt.figure(1)
        plt.cla()
        plt.ylim(-9000, 9000)
        plt.xlim(-9000, 9000)
        plt.scatter(x, y, c='r', s=8)
        plt.pause(0.001)
    plt.close("all")


is_plot = True
x = []
y = []

for _ in range(430):
    x.append(0)
    y.append(0)

with open("../../Data/data_2.json", "r") as st_json:
    ldata = json.load(st_json)

    cnt = 0
    prevsf = 0
    startTimestamp = 0

#    camera = Camera(plt.figure())

    ischecked = False
    inputdata = []
    for data in ldata['rawdata']:
        if startTimestamp == 0:
            startTimestamp = data['timestamp']
        ctimestamp = data['timestamp']
        tgap = ctimestamp - startTimestamp

        if tgap > 3.0 and data['start_flag'] == True and cnt != 0:
            gap = cnt - prevsf
            #print(cnt, gap, data)
            prevsf = cnt
            if ischecked == False:
                ischecked = True
            else:
                ischecked = False

                cnt = 0
                for data in inputdata:
                    x[cnt] = data['distance'] * math.cos(math.radians(90-data['angle']))
                    y[cnt] = data['distance'] * math.sin(math.radians(90-data['angle']))
                    #print(x[cnt], y[cnt])
                    cnt += 1

                print("Draw Graph",cnt)
                plt.ylim(-4000, 8000)
                plt.xlim(-4000, 4000)
                plt.scatter(x, y, c='r', s=1)
                plt.show()
 #               camera.snap()

                inputdata.clear()
                break

        if ischecked:
            inputdata.append(data)

        cnt += 1

    print(len(inputdata))

   # threading.Thread(target=draw).start()

#    anim = camera.animate(blit=True)
#    anim.save('scatter.mp4')

#    anim = camera.animate(blit=True)
#    anim.save('animation.gif', writer='PillowWriter', fps=2)