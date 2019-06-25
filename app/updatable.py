# This class does ...

from time import time

class Updatable:
    def __init__(self, updatefunc, interval=600, update=False):
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

    def __call__(self, key=None):
        # Return data
        if self.outdated():
            self.update()
        if key == None:
            return self.mydata
        elif key in self.mydata:
            return self.mydata[key]
        else:
            return None

    def outdated(self):
        if self.mydata == None:
            return True
        return (time()-self.updatetime) > self.interval
