import re
import sys
import queue

import sys
sys.path.append("./Message/")

from PlayerMode import PlayerMode
from Response import Response

class ParticipantModel:

    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        self.score = 0
        self.nickname = None
        self.mode = PlayerMode.WAIT
        self.responses = queue.Queue()

    def __str__(self):
        return f"ParticipantModel({self.nickname}, {self.address})"

    def getMode(self) -> PlayerMode:
        return self.mode

    @staticmethod
    def checkNicknameValid(nickname: str) -> bool:
        length = len(nickname)
        return (1 <= length) and (length <= 10) and re.match("^[a-zA-Z0-9_]*$", nickname)

    def setNickname(self, nickname: str) -> bool:
        if self.checkNicknameValid(nickname):
            self.nickname = nickname
            return True
        return False
    
    def getNickname(self) -> str:
        return self.nickname
    
    def reset(self):
        self.score = 0
        self.mode = PlayerMode.PLAY

    def wait(self):
        self.mode = PlayerMode.WAIT
        
    def increaseScore(self, score : int):
        self.score += score
        
    def die(self):
        self.mode = PlayerMode.DIE
        
    def becomeWatcher(self) -> None:
        self.mode = PlayerMode.WATCH
    
    def addResponse(self, message):
        self.responses.put(message)
    
    def isWatcher(self):
        return self.mode == PlayerMode.WATCH
    
    def isWaiting(self):
        return self.mode == PlayerMode.WAIT

    def isAlive(self) -> bool:
        return self.mode != PlayerMode.DIE

    def sendResponse(self, socket) -> bool:

        if not self.responses.empty():

            message = self.responses.get().toString().encode("utf-8")

            length = len(message)

            message += b" " * (1024 - length)

            try:
                socket.sendall(message)

                print(f"[SERVER] Sent message: {message}")
         
            except:
                return False
            
            return True

        return False
    
    def containsUnsentResponse(self) -> bool:
        return not self.responses.empty()