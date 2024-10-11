import os



class FIFO:
    def __init__(self, path: str):
        self.lock_r=False
        self.lock_w=False
        self.path=os.path.abspath(path)
    def read(self):
        while True:
            if not self.lock_r:
                break
        self.lock_r = True
        with open(self.path, "r") as fifo:
            c=fifo.read()
        self.lock_r = False
        return c
    def write(self, content: str):
        while True:
            if not self.lock_w:
                break
        self.lock_w = True
        with open(self.path, "r") as fifo:
            fifo.write(content)
            fifo.flush()
        self.lock_w = False
        
    