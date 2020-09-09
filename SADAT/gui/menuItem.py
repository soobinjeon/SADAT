from abc import *

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction


class MenuItem(metaclass=ABCMeta):

    def __init__(self, name, menuobject, parent):
        self.menubar = menuobject
        self.name = name
        self.parent = parent
        self.Action = QAction(self.name, self.parent)
        self.Action.triggered.connect(self.trigger)
        #self.menubar.addAction(self.Action)

    def test(self):

        pass

    def getAction(self):
        return self.Action

    @abstractmethod
    def trigger(self):
        print("Super test")
        pass