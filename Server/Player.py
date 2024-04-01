import re

class Player:
    def __init__(self):
        self.score = 0
        self.nickname = None

    def setNickname(self, nickname: str) -> bool:
        length = len(nickname)
        if (length <= 0) or (length > 10) or (not re.match("^[a-zA-Z0-9_]*$", nickname)):
            return False
        self.nickname = nickname
        return True
    
    def getNickname(self):
        return self.nickname