import sys
import random

class Quiz:
    
    def __init__(self, question : str, keyword : str):
        self.question = question.strip()
        self.keyword = keyword.strip().upper()

    def countOccernerces(self, character : str) -> int:
    
        if len(character) != 1:
            return 0
    
        return self.keyword.count(character)
        
    def getQuestion(self) -> str:
        return self.question
    
    def getKeyword(self) -> str:
        return self.keyword
    
    def __str__(self) -> str:
        return f"{self.keyword}: {self.question}"
    
    def __repr__(self) -> str:
        return f"Quiz(keyword = {self.keyword}, question = {self.question})"