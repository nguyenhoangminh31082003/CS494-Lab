import sys
import random

class Quiz:
    def __init__(self, question, keyword):
        self.question = question.strip()
        self.keyword = keyword.strip().upper()
        self.encoded = "*" * len(keyword)
    
    def guessLetter(self, letter) -> bool:
        if letter.strip().upper() in self.keyword:
            self.updateEncoded(letter)
            return True
        else:
            return False
    
    def guessKeyword(self, keyword) -> bool:
        if keyword.strip().upper() == self.keyword:
            self.encoded = self.keyword
            return True
        else:
            return False
    
    def updateEncoded(self, letter) -> None:
        raise NotImplementedError
    
    def getQuestion(self) -> str:
        raise NotImplementedError