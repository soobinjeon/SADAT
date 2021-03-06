import sys

from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

import SnSimulator
from gui.EventHandler import MouseEventHandler
from gui.menuExit import menuExit
from gui.menuFiles import menuLoadSim, menuLogPlay
from gui.menuSim import menuSim

from multiprocessing import Manager

from gui.toolbarOption import toolbarPlay, toolbarEditor
from gui.toolbarSlider import toolbarSlider

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
        self.cmode = self.STOPMODE

    def addToolbar(self, item, name):
        self.toolbar[name] = item

    def addMenubar(self, item, name):
        self.menubar[name] = item

    def addSlider(self, item):
        self.slider = item

    def getSlider(self):
        return self.slider

    def getCurrentMode(self):
        return self.cmode

    def setPlayMode(self, mode):
        self.cmode = mode
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

class MyAppEventManager():
    def __init__(self):
        pass

class MyWG(QWidget):

    def __init__(self, parent):
        super(MyWG, self).__init__(parent)
        self.pr = parent
        self.initUI()

    def initUI(self):
        self.group=QGroupBox("Evaluation")
        self.group.setStyleSheet("color:black;"
                                 "background-color: white;")
        fInnerLayOut=QVBoxLayout()
        self.buttonGroup=QGroupBox("Vehicle Button")
        self.buttonGroup.setStyleSheet("color:green;"
                                       "background-color: gray")
        self.pushButton1 = QPushButton("전진")
        self.pushButton2 = QPushButton("후진")
        self.pushButton3 = QPushButton("좌회전")
        self.pushButton4 = QPushButton("우회전")
        self.pushButton5 = QPushButton("멈춤")

        eInnerLayOut=QVBoxLayout()
        eInnerLayOut.addWidget(self.pushButton1)
        eInnerLayOut.addWidget(self.pushButton2)
        eInnerLayOut.addWidget(self.pushButton3)
        eInnerLayOut.addWidget(self.pushButton4)
        eInnerLayOut.addWidget(self.pushButton5)
        self.buttonGroup.setLayout(eInnerLayOut)
        self.ExGroup=QGroupBox("None")
        self.ExGroup.setStyleSheet("color:green;"
                                   "background-color: gray")
        fInnerLayOut.addWidget(self.buttonGroup)
        fInnerLayOut.addWidget(self.ExGroup,1)
        self.group.setLayout(fInnerLayOut)
        layout=QVBoxLayout()
        layout.addWidget(self.group)
        self.setLayout(layout)
        self.setFixedSize(300, 730)

        self.pr.guiGroup[GUI_GROUP.LOGGING_MODE] = []
        self.pr.guiGroup[GUI_GROUP.LOGPLAY_MODE] = []


        self.pr.statusBar()
        self.pr.statusBar().setStyleSheet("background-color : white")
        self.pr.initMenubar()
        self.pr.initToolbar()
        self.pr.initplanview()
        self.pr.setStyleSheet("""QMenuBar {
                 background-color: Gray;
                 color: white;
                }

             QMenuBar::item {
                 background: Gray;
                 color: white;
             }""")

        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.pr.setPalette(p)
        #self.setPalette(p)
        self.pr.modeChanger(GUI_GROUP.ALL, False)

        self.setWindowTitle('QGridLayout')
        self.setGeometry(300, 300, 300, 200)
        self.show()

    # def paintEvent(self, e):
    #     qp = QPainter()
    #     qp.begin(self)
    #     self.draw_point(qp)
    #     qp.end()


class MyApp(QMainWindow):

    def __init__(self, parent=None):
        super(MyApp, self).__init__(parent)

        #for Planview Size and Position
        self.panviewSize = 10
        self.relx = 0
        self.rely = 0

        #frame rate
        self.velocity = 15
        #init gui group
        self.guiGroup = {}

        self.gcontrol = GUI_CONTROLLER()
        self.mouseEventHndl = MouseEventHandler()

        self.xpos = []
        self.ypos = []

        # init Simulator Manager
        self.simulator = SnSimulator.SnSimulator(Manager(), self)
        self.simulator.setVelocity(self.velocity)

        self.form_widget = MyWG(self)
        self.setCentralWidget(self.form_widget)
        self.initUI()

    def initUI(self):
        #init gui group
        # self.guiGroup[GUI_GROUP.LOGGING_MODE] = []
        # self.guiGroup[GUI_GROUP.LOGPLAY_MODE] = []
        #
        # self.statusBar()
        # self.statusBar().setStyleSheet("background-color : white")
        # self.initMenubar()
        # self.initToolbar()
        # self.initplanview()
        # self.setStyleSheet("""QMenuBar {
        #          background-color: Gray;
        #          color: white;
        #         }
        #
        #      QMenuBar::item {
        #          background: Gray;
        #          color: white;
        #      }""")
        #
        # p = self.palette()
        # p.setColor(self.backgroundRole(), Qt.black)
        # self.setPalette(p)
        # self.modeChanger(GUI_GROUP.ALL, False)
        self.setWindowTitle('SADAT')
        #self.setStyleSheet("background-color: dimgray;")
        self.setGeometry(300, 300, 1500, 1000)
        self.show()

    def initMenubar(self):
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        self.statusBar()

        #File Menu
        filemenu = menubar.addMenu('&File')
        filemenu.addAction(menuLoadSim('Load log files..', self))
        filemenu.addAction(menuLogPlay('Log Play',self))
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
        self.toolvel = toolbarEditor('10', self, self.simulator.setVelocity)
        self.toolvel.setText(str(self.simulator.getVelocity()))

        self.toolbar.addAction(toolplay)
        self.toolbar.addAction(toolpause)
        self.toolbar.addAction(toolresume)
        self.toolbar.addWidget(self.toolvel)
        self.toolbar.setStyleSheet("color: white")

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
        grid_layout = QGridLayout()
        self.setLayout(grid_layout)

        for x in range(3):
            for y in range(3):
                button = QPushButton(str(str(3 * x + y)))
                grid_layout.addWidget(button, x, y)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw_point(qp)
        qp.end()

    #event
    def wheelEvent(self, e):
        wvalue = e.angleDelta().y()
        div = 0.025
        max = 0.6
        min = 0.05
        dv = wvalue * div
        if dv != 0:
            sign = abs(dv) / dv
        else:
            sign = 0

        if abs(dv) > max:
            dv = max * sign
        elif abs(dv) < min:
            dv = min * sign

        temp = self.panviewSize + dv

        if 0.1 < temp <= 126:
            self.panviewSize += dv

        if self.gcontrol.getCurrentMode() is not GUI_CONTROLLER.PLAYMODE:
            self.updatePosition()

    def mouseMoveEvent(self, e):
        pass
        # mevent = self.mouseEventHndl.moveEvent
        #
        # if e.buttons() == Qt.LeftButton:
        #     if mevent.eventMouse(e.globalX(), e.globalY()):


    def draw_point(self, qp):
        #draw paint
        qp.setPen(QPen(Qt.white, 1))


        for idx,item in enumerate(self.xpos):
            #qp.drawPoint(int(self.xpos[idx]), int(self.ypos[idx]))
            xp = int(self.xpos[idx])+150    #
            yp = int(self.ypos[idx])+100
            xw = xp + 1
            yw = yp + 1
            #print(self.panviewSize, xp, yp)
            qp.drawEllipse(xp, yp, 1, 1)

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
        self.prevx = data[0]
        self.prevy = data[1]

        self.updatePosition()

    def updatePosition(self):
        # print(len(x))
        self.xpos.clear()
        self.ypos.clear()

        for idx, item in enumerate(self.prevx):
            self.xpos.append((self.prevx[idx] / self.panviewSize) + (self.width() / 2) + self.relx)
            self.ypos.append((self.prevy[idx] / self.panviewSize) + (self.height() / 2) + self.rely)

        self.update()

    def playbackstatus(self, pbinfo):
        if pbinfo.mode == self.simulator.lpthread.PLAYMODE_LOAD:
            self.gcontrol.getSlider().setSliderRange(pbinfo.maxLength)
            self.velocity = pbinfo.setfps
            self.simulator.setVelocity(self.velocity)
            self.toolvel.setText(str(self.simulator.getVelocity()))

            self.modeChanger(GUI_GROUP.LOGPLAY_MODE, True)
        elif pbinfo.mode == self.simulator.lpthread.PLAYMODE_PLAY:
            self.gcontrol.getSlider().setValue(pbinfo.currentIdx)
        elif pbinfo.mode == self.simulator.lpthread.PLAYMODE_SETVALUE:
            pass
        stxt = 'current idx - %d'%pbinfo.currentIdx
        self.statusBar().showMessage(stxt)
        self.update()
        #print("pbInfo : ", pbinfo.mode, pbinfo.maxLength, pbinfo.currentIdx)

    def closeEvent(self, event):
        sys.exit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())