class Channel:
    def __init__(self):
        self.var =  []

    def set(self, value):
        self.var[0] = value
    def get(self):
        return self.var[0]
