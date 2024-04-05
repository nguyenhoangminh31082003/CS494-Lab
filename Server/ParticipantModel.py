import re
import sys
import queue

import sys
sys.path.append("./Message/")

from Mode import Mode
from Response import Response

class ParticipantModel:

    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        self.score = 0
        self.nickname = None
        self.mode = Mode.WATCH
        self.responses = queue.Queue()

    def __str__(self):
        return f"ParticipantModel({self.nickname}, {self.address})"

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
        self.mode = Mode.PLAY
        
    def increaseScore(self, score : int):
        self.score += score
        
    def wrongAnswerKeyword(self):
        self.mode = Mode.DIE
        
    def becomeWatcher(self) -> None:
        self.mode = Mode.WATCH
    
    def addResponse(self, message):
        self.responses.put(message)

    def isAlive(self) -> bool:
        return self.mode != Mode.DIE

    def sendResponse(self, socket) -> bool:

        if not self.responses.empty():

            message = self.responses.get().toString().encode("utf-8")

            #Somehow we need this line to avoid an error at client when client tries to deserialize the message
            print(f"[SERVER] Sending response to {self.nickname} ({self.address}): {message}")

            try:
                socket.sendall(message)
            except:
                return False
            
            return True

        return False