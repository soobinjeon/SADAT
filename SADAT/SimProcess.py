class SimProcess:
    name = ""
    target = None
    args = None
    def __init__(self, name, target, args):
        self.name = name
        self.target = target
        self.args = args