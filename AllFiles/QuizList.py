import sys
import random
import json

from Quiz import Quiz
from CurrentQuiz import CurrentQuiz

class QuizList:

    def __init__(self):
        self.quizzes = []
        self.readQuizzes()
        self.currentQuiz = None
    
    def getJSONSummary(self) -> dict:

        result = {
            "keyword_length": self.currentQuiz.getKeywordLength(),
            "current_keyword": self.currentQuiz.getCurrentKeyword(),
            "keyword": self.currentQuiz.getKeyword(),
            "hint": self.currentQuiz.getQuestion()
        }

        return result

    def readQuizzes(self) -> None:
        with open("Data/data.txt", "r") as file:
            self.quizzes.clear()

            wordCount = int(file.readline())

            for _ in range(wordCount):
                k = file.readline()
                q = file.readline()
                
                self.quizzes.append(Quiz(
                    question = q,
                    keyword = k
                ))

            random.shuffle(self.quizzes)

    def chooseRandomQuiz(self) -> None:
        self.currentQuiz = CurrentQuiz(random.choice(self.quizzes))

    def receiveLetterGuess(self, letter : str) -> bool:
        return self.currentQuiz.receiveLetterGuess(letter)
    
    def receiveKeywordGuess(self, keyword : str) -> bool:    
        return self.currentQuiz.receiveKeywordGuess(keyword)
    
    def getFormattedSummary(self) -> str:
        return "\n".join([
            f"The length of the keyword is {self.currentQuiz.getKeywordLength()}: {self.currentQuiz.getCurrentKeyword()}",
            f"Hint: {self.currentQuiz.getQuestion()}"
        ])

    def getSerializedQuestion(self) -> str:
        return json.dumps({
            "question": self.currentQuiz.getQuestion(),
            "keyword": self.currentQuiz.getCurrentKeyword()
        })
    
    def getCurrentQuiz(self) -> CurrentQuiz:
        return self.currentQuiz