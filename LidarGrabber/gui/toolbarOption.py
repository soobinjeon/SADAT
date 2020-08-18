from PyQt5.QtWidgets import QAction


class toolbarPlay(QAction):

    def __init__(self, name, parent, func=None, shortcut=None):
        super().__init__(name, parent)
        self.parent = parent
        if func is not None:
            self.triggered.connect(func)

        if shortcut is not None:
            self.setShortcut(shortcut)
        #self.setStatusTip('Play Sim')