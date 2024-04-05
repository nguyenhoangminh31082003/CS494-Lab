import sys
import random

class Quiz:
    
    def __init__(self, question : str, keyword : str):
        self.question = question.strip()
        self.keyword = keyword.strip().upper()
        
    def getQuestion(self) -> str:
        raise self.question
    
    def getKeyword(self) -> str:
        raise self.keyword