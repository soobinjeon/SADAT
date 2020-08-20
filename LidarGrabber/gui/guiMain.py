import sys

from PyQt5.QtGui import QIcon, QPainter, QPen
from PyQt5.QtWidgets import QApplication, QMainWindow, qApp, QAction, QSlider
from PyQt5.QtCore import Qt, QTimer

import SnSimulator
from gui.menuExit import menuExit
from gui.menuLoadSim import menuLoadSim
from gui.menuSim import menuSim

from multiprocessing import Manager

from gui.toolbarOption import toolbarPlay, toolbarEditor
from gui.toolbarSlider import toolbarSlider
from taskPlanview import taskPlanview

class GUI_GROUP:
    ALL = 0
    LOGGING_MODE = 1
    LOGPLAY_MODE = 2

class GUI_CONTROLLER:
    STOPMODE = 0
    PLAYMODE = 1
    RESUMEMODE = 2

    def __init__(self):
        self.toolbar = {}
        self.menubar = {}
        self.slider = None

    def addToolbar(self, item, name):
        self.toolbar[name] = item

    def addMenubar(self, item, name):
        self.menubar[name] = item

    def addSlider(self, item):
        self.slider = item

    def getSlider(self):
        return self.slider

    def setPlayMode(self, mode):
        if mode is self.STOPMODE:
            self.toolbar['Play'].setVisible(True)
            self.toolbar['Pause'].setVisible(False)
            self.toolbar['Resume'].setVisible(False)
        elif mode is self.PLAYMODE:
            self.toolbar['Play'].setVisible(False)
            self.toolbar['Pause'].setVisible(True)
            self.toolbar['Resume'].setVisible(False)
        else:
            self.toolbar['Play'].setVisible(False)
            self.toolbar['Pause'].setVisible(False)
            self.toolbar['Resume'].setVisible(True)

class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()

        #init gui group
        self.guiGroup = {}

        self.gcontrol = GUI_CONTROLLER()

        self.xpos = []
        self.ypos = []

        # init Simulator Manager
        self.simulator = SnSimulator.SnSimulator(Manager(), self)
        self.simulator.setVelocity(60)

        self.initUI()

    def initUI(self):
        #init gui group
        self.guiGroup[GUI_GROUP.LOGGING_MODE] = []
        self.guiGroup[GUI_GROUP.LOGPLAY_MODE] = []

        self.statusBar()
        self.initMenubar()
        self.initToolbar()
        self.initplanview()
        #self.timer = QTimer(self)
        #self.timer.timeout.connect(self.changePosition)
        #self.timer.start(int(1000 / self.vel))
        self.modeChanger(GUI_GROUP.ALL, False)
        self.setWindowTitle('Lidar Cluster')
        #self.setStyleSheet("background-color: dimgray;")
        self.setGeometry(300, 300, 1000, 1000)
        self.show()

    def initMenubar(self):
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        self.statusBar()

        #File Menu
        filemenu = menubar.addMenu('&File')
        filemenu.addAction(menuLoadSim('Load log files..',self))
        filemenu.addAction(menuExit('exit', self))

        #Simulation Menu
        simmenu = menubar.addMenu('&Simulation')
        simmenu.addAction(menuSim('Play',self))
        self.guiGroup[GUI_GROUP.LOGPLAY_MODE].append(simmenu)

    def initToolbar(self):
        self.toolbar = self.addToolBar('Navigator')
        toolplay = toolbarPlay('Play', self, self.simulator.playMode, 'Ctrl+P')
        toolpause = toolbarPlay('Pause', self, self.simulator.PauseMode)
        toolresume = toolbarPlay('Resume', self, self.simulator.ResumeMode)
        toolvel = toolbarEditor('10', self, self.simulator.setVelocity)
        toolvel.setText(str(self.simulator.getVelocity()))
        self.toolbar.addAction(toolplay)
        self.toolbar.addAction(toolpause)
        self.toolbar.addAction(toolresume)
        self.toolbar.addWidget(toolvel)

        #slider
        slider = toolbarSlider(Qt.Horizontal, self)
        slider.sliderMoved.connect(self.sliderMoved)
        slider.sliderReleased.connect(self.sliderMoved)
        self.toolbar.addWidget(slider)

        self.gcontrol.addToolbar(toolplay, toolplay.text())
        self.gcontrol.addToolbar(toolpause, toolpause.text())
        self.gcontrol.addToolbar(toolresume, toolresume.text())
        self.gcontrol.addToolbar(slider, 'logslider')
        self.gcontrol.addSlider(slider)
        self.gcontrol.setPlayMode(GUI_CONTROLLER.STOPMODE)

        self.guiGroup[GUI_GROUP.LOGPLAY_MODE].append(self.toolbar)


    def initplanview(self):
        pass

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw_point(qp)
        qp.end()

    def draw_point(self, qp):
        #print('draw paint')
        qp.setPen(QPen(Qt.black, 2))

        for idx,item in enumerate(self.xpos):
            qp.drawPoint(int(self.xpos[idx]), int(self.ypos[idx]))

    def modeChanger(self, mode, isTrue):
        for modedata in self.guiGroup:
            if mode is GUI_GROUP.ALL or modedata is mode:
                for actions in self.guiGroup[modedata]:
                    actions.setEnabled(isTrue)

    def setStatus(self, str):
        self.statusBar().showMessage(str)

    #Callback Event

    def sliderMoved(self):
        self.simulator.lpthread.setPlayPoint(self.gcontrol.getSlider().value())
        self.simulator.PauseMode()

    def changePosition(self, data):
        x = data[0]
        y = data[1]
        self.xpos.clear()
        self.ypos.clear()

        #print(len(x))
        for idx, item in enumerate(x):
            self.xpos.append((x[idx] / 15) + (self.width() / 2))
            self.ypos.append((y[idx] / 15) + (self.height() / 2))

        #print(self.target_x_pos, self.target_y_pos)
        self.update()

    def playbackstatus(self, pbinfo):
        if pbinfo.mode == self.simulator.lpthread.PLAYMODE_LOAD:
            self.gcontrol.getSlider().setSliderRange(pbinfo.maxLength)
            self.modeChanger(GUI_GROUP.LOGPLAY_MODE, True)
        elif pbinfo.mode == self.simulator.lpthread.PLAYMODE_PLAY:
            self.gcontrol.getSlider().setValue(pbinfo.currentIdx)
        elif pbinfo.mode == self.simulator.lpthread.PLAYMODE_SETVALUE:
            pass
        stxt = 'current idx - %d'%pbinfo.currentIdx
        self.statusBar().showMessage(stxt)
        self.update()
        #print("pbInfo : ", pbinfo.mode, pbinfo.maxLength, pbinfo.currentIdx)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())