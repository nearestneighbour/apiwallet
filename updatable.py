from time import time


class updatable:
    def __init__(self, updatefunc, interval, update=True):
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

    @property
    def data(self):
        # Get data
        if self.outdated:
            self.update()
        return self.mydata

    @property
    def outdated(self):
        if self.mydata == None:
            return True
        return (time()-self.updatetime) > self.interval
