from events import *


class RunnerController(object):
    """The heart beat of the application. Used to keep the application running until a quit event"""

    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)

        self.keepGoing = 1

    def Run(self):
        while self.keepGoing:
            event = TickEvent()
            self.evManager.Post(event)

    def Notify(self, event):
        if isinstance(event, QuitEvent):
            #this will stop the while loop from running
            self.keepGoing = False
