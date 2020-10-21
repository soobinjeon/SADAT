class MouseEventHandler:
    def __init__(self):
        self.moveEvent = MouseMoveEvent()


class MouseMoveEvent:
    def __init__(self):
        self.X = 0
        self.Y = 0

    def eventMouse(self, xpos, ypos):
        if self.X != xpos or self.Y != ypos:
            self.X = xpos
            self.Y = ypos
            return True
        else:
            return False
