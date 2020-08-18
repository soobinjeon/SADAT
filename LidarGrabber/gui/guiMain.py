import sys

from PyQt5.QtGui import QIcon, QPainter, QPen
from PyQt5.QtWidgets import QApplication, QMainWindow, qApp, QAction, QSlider
from PyQt5.QtCore import Qt, QTimer

from SnSimulator import SnSimulator
from gui.menuExit import menuExit
from gui.menuSim import menuSim

from multiprocessing import Manager

from gui.toolbarOption import toolbarPlay
from gui.toolbarSlider import toolbarSlider
from taskPlanview import taskPlanview


class MyApp(QMainWindow):
    vel = 30

    def __init__(self):
        super().__init__()

        self.xpos = []
        self.ypos = []

        # init Simulator Manager
        self.simulator = SnSimulator(Manager(), self)
        self.simulator.setVelocity(10)

        self.initUI()

    def initUI(self):
        self.statusBar()
        self.initMenubar()
        self.initToolbar()
        self.initplanview()

        self.timer = QTimer(self)
        #self.timer.timeout.connect(self.changePosition)
        self.timer.start(int(1000 / self.vel))

        self.setWindowTitle('Lidar Cluster')
        self.setGeometry(300, 300, 1000, 1000)
        self.show()

    def initMenubar(self):
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        self.statusBar()

        #File Menu
        filemenu = menubar.addMenu('&File')
        filemenu.addAction(menuExit('exit',self))

        #Simulation Menu
        simmenu = menubar.addMenu('&Simulation')
        simmenu.addAction(menuSim('PlaySim',self))

    def initToolbar(self):
        self.toolbar = self.addToolBar('Navigator')
        self.toolbar.addAction(toolbarPlay('Play', self, self.simulator.playMode, 'Ctrl+P'))
        self.toolbar.addAction(toolbarPlay('Pause', self, self.simulator.PauseMode))
        #slider
        self.slider = toolbarSlider(Qt.Horizontal, self)
        self.toolbar.addWidget(self.slider)


    def initplanview(self):
        for i in range(1000):
            self.xpos.append(0)
            self.ypos.append(0)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw_point(qp)
        qp.end()

    def draw_point(self, qp):
        qp.setPen(QPen(Qt.blue, 2))

        for idx,item in enumerate(self.xpos):
            qp.drawPoint(int(self.xpos[idx]), int(self.ypos[idx]))

    def changePosition(self, data):
        x = data[0]
        y = data[1]

        for idx, item in enumerate(x):
            self.xpos[idx] = (x[idx] / 15) + (self.width() / 2)
            self.ypos[idx] = (y[idx] / 15) + (self.height() / 2)

        #print(self.target_x_pos, self.target_y_pos)
        self.update()

    def playbackstatus(self, pbinfo):
        if pbinfo.mode == 0:
            self.slider.setSliderRange(pbinfo.maxLength)
        else:
            self.slider.setValue(pbinfo.currentIdx)
        self.update()
        #print("pbInfo : ", pbinfo.mode, pbinfo.maxLength, pbinfo.currentIdx)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())