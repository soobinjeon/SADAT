from PyQt5.QtWidgets import QAction, QLineEdit


class toolbarPlay(QAction):

    def __init__(self, name, parent, func=None, shortcut=None):
        super().__init__(name, parent)
        self.parent = parent
        if func is not None:
            self.triggered.connect(func)

        if shortcut is not None:
            self.setShortcut(shortcut)


        #self.setStatusTip('Play Sim')

class toolbarEditor(QLineEdit):

    def __init__(self, name, parent, func=None, shortcut=None):
        super().__init__(name, parent)
        self.parent = parent
        self.setFixedWidth(50)
        self.setStyleSheet("color: black")
        if func is not None:
            self.returnPressed.connect(lambda: func(self.text()))

        if shortcut is not None:
            self.setShortcut(shortcut)
        #self.setStatusTip('Play Sim')