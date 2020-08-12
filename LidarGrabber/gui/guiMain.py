import sys
from multiprocessing import Manager

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, qApp, QAction

from SnSimulator import SnSimulator
from gui.menuExit import menuExit
from gui.menuSim import menuSim


class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.statusBar()
        self.initMenubar()

        self.setWindowTitle('Lidar Cluster')
        self.setGeometry(300, 300, 1000, 1000)
        self.show()

        gm = SnSimulator(Manager())

    def initMenubar(self):
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)

        #File Menu
        filemenu = menubar.addMenu('&File')
        filemenu.addAction(menuExit('exit',self))

        #Simulation Menu
        simmenu = menubar.addMenu('&Simulation')
        simmenu.addAction(menuSim('PlaySim',self))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())