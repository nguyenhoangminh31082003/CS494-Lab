import re
import sys
sys.path.append("../")
from Server.Score import * 
from Server.Mode import Mode

class ClientModel:
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        self.score = 0
        self.nickname = None
        self.mode = Mode.WATCH

    def setNickname(self, nickname: str) -> bool:
        length = len(nickname)
        if (length <= 0) or (length > 10) or (not re.match("^[a-zA-Z0-9_]*$", nickname)):
            return False
        self.nickname = nickname
        return True
    
    def getNickname(self):
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
        