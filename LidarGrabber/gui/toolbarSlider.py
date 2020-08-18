from PyQt5.QtWidgets import QAction, QSlider


class toolbarSlider(QSlider):

    def __init__(self, dir, parent):
        super().__init__(dir, parent)
        self.parent = parent
        self.valueChanged.connect(self.trig)
        self.setRange(0, 100)
        self.setSingleStep(1)

    def setSliderRange(self, maxLength):
        self.setRange(0, maxLength)

    def trig(self, val):
        pass
        #print(val)