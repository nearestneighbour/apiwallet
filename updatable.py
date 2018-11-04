from time import time


class updatable:
    def __init__(self, updatefunc, interval, update=True):
        self.updatefunc = updatefunc
        if update:
            self.update() # Set self.data and self.updatetime
        else:
            self.data = None
            self.updatetime = None
        self.interval = interval

    def update(self, interval=None):
        # Set data
        self.data = self.updatefunc()
        if interval != None:
            self.interval = interv
        self.updatetime = time()

    def getdata(self, update=True):
        # Get data
        if update and self.outdated():
            self.update()
        return self.data

    def outdated(self):
        if self.data == None:
            return True
        return (time()-self.updatetime) > self.interval
