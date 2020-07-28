from tkinter import *
import time

class Planview:
    def __init__(self):
        self.cwidth = 1000
        self.cheight = 1000

        self.window = Tk()
        self.canvas = Canvas(self.window, width=self.cwidth, height=self.cheight)
        self.canvas.pack()

        self.nofnode = 400
        self.nodes = []

        self.circleSX = 0
        self.circleSY = 0

        self.circleSizeX = 10
        self.circleSizeY = 10

    def drawCrossline(self, lq):
        coord = [0, (self.cheight / 2), self.cwidth, (self.cheight / 2)]
        line1 = self.canvas.create_line(coord, fill="Black")

        coord = [(self.cwidth / 2), 0, (self.cwidth / 2), self.cheight]
        line2 = self.canvas.create_line(coord, fill="Black")

        for data in iter(lq.get, 'interrupt'):
            xy = data
            x = xy[0]
            y = xy[1]
            #print(x)
            #print(y)
            for icnt in range(len(x)):
                # draw circle

                sX = x[icnt] / 15
                sY = y[icnt] / 15
                sizeX = sX + self.circleSizeX
                sizeY = sY + self.circleSizeY

                sX = sX + (self.cwidth/2)
                sizeX = sizeX + (self.cwidth/2)
                sY = sY + (self.cheight/2)
                sizeY = sizeY + (self.cheight/2)
                self.nodes.append(self.canvas.create_oval(sX, sY, sizeX , sizeY, fill='green'))
                #self.canvas.itemconfigure(self.nodes[x], state='hidden')
            break

    def do_one_frame(self, lq):
        self.canvas.delete("all")
        self.drawCrossline(lq)
        self.canvas.after(200, self.do_one_frame, lq)

    def paintPlanview(self):
        rd = Reader()

        manager = Manager()
        lidarDataQueue = manager.Queue()

        processes = []
        processes.append(Process(name="GUI", target=rd.startRead, args=(1, lidarDataQueue)))

        for p in processes:
            p.start()
            print("Start", p, p.is_alive())

        #self.drawCrossline()
        self.do_one_frame(lidarDataQueue)
        #
        # for i in range(100):
        #     self.canvas.move(oval, 3, 0)
        #     self.window.update()
        #     time.sleep(0.05)
        #
        # for i in range(100):
        #     self.canvas.move(oval, -3, 0)
        #     self.window.update()
        #     time.sleep(0.001)



        self.window.mainloop()

        for p in self.processes:
            p.join()
        print("end Process")