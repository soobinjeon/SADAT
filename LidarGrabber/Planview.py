from tkinter import *
import time

from menubartest import App


class Planview:
    def __init__(self):
        self.cwidth = 700
        self.cheight = 700

        self.window = Tk()

        self.drawMenu()

        self.canvas = Canvas(self.window, width=self.cwidth, height=self.cheight)
        self.canvas.pack()

        self.nofnode = 400
        self.nodes = []

        self.circleSX = 0
        self.circleSY = 0

        self.circleSizeX = 10
        self.circleSizeY = 10


    def donothing(self):
        print("do nothing")

    def drawMenu(self):
        print("Draw Menu")
        self.window.title("Lidar Simulator")
        app = App(self.window)

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
        #self.drawCrossline(lq)
        self.canvas.after(200, self.do_one_frame, lq)

    def paintPlanview(self):
        #self.do_one_frame(None)
        self.window.mainloop()