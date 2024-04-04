import re
import sys

from Server.Score import * 
from Server.Mode import Mode

class PlayerModel:

    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        self.score = 0
        self.nickname = None
        self.mode = Mode.WATCH

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
        