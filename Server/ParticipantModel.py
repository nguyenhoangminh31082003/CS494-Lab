import re
import sys
import queue

from Score import * 
from Mode import Mode

class ParticipantModel:

    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        self.score = 0
        self.nickname = None
        self.mode = Mode.WATCH
        self.messagesToBeSent = queue.Queue()

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
        
    def correctAnswerLetter(self):
        self.score += LETTER_SCORE
        
    def correctAnswerKeyword(self):
        self.score += KEYWORD_SCORE
        
    def wrongAnswerKeyword(self):
        self.mode = Mode.DIE
        
    def becomeWatcher(self) -> None:
        self.mode = Mode.WATCH

    def getMessageToBeSent(self):
        if not self.messagesToBeSent.empty():
            return self.messagesToBeSent.get()
        return None
    
    def addMessageToBeSent(self, message):
        self.messagesToBeSent.put(message)

    def sendMessageWithGivenSocket(self, socket) -> bool:

        if not self.messagesToBeSent.empty():
            message = self.messagesToBeSent.get()
            try:
                socket.sendall(message.encode("utf-8"))
            except:
                return False
            return True

        return False