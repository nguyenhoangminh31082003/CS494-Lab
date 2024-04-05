import sys
import random

from Quiz import Quiz
from CurrentQuiz import CurrentQuiz

class QuizList:

    def __init__(self):
        self.quizzes = []
        self.readQuizzes()
        self.currentQuiz = None
    
    def readQuizzes(self) -> None:
        with open("data.txt", "r") as file:
            self.quizzes.clear()

            wordCount = int(file.readline())

            for _ in range(wordCount):
                line = file.readline()
                position = line.find(":")
                self.quizzes.append(Quiz(
                    question = line[(position + 1):],
                    keyword = line[:position]
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