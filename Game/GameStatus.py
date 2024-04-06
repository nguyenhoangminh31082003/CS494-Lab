import enum

class GameStatus(enum.IntEnum):
    OFF = 0,
    READY = 1,
    RUNNING = 2

    def isOff(self):
        return self == GameStatus.OFF
    
    def isReady(self):
        return self == GameStatus.READY
    
    def isRunning(self):
        return self == GameStatus.RUNNING
    
    def isNotOff(self):
        return self != GameStatus.OFF