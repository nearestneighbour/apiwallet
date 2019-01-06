# This class does ...

from time import time

class Updatable:
    def __init__(self, updatefunc, interval=300, update=False):
        self.updatefunc = updatefunc
        if update:
            self.update() # Set self.data and self.updatetime
        else:
            self.mydata = None
            self.updatetime = None
        self.interval = interval

    def update(self, interval=None):
        # Set data
        self.mydata = self.updatefunc()
        if interval != None:
            self.interval = interval
        self.updatetime = time()

    def __call__(self):
        # Return data
        if self.outdated():
            self.update()
        return self.mydata

    def outdated(self):
        if self.mydata == None:
            return True
        return (time()-self.updatetime) > self.interval
