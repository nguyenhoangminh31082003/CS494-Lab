import sys
import random

from Quiz import Quiz

class QuizList:

    def __init__(self):
        self.quizzes = []
        self.readQuizzes()
        self.currentQuizIndex = 0
    
    def readQuizzes(self) -> None:
        with open("data.txt", "r") as file:
            self.quizzes.clear()

            wordCount = int(file.readline())

            for _ in range(wordCount):
                tmp = file.readline().split(":")
                self.quizzes.append(Quiz(tmp[0], tmp[1]))

            random.shuffle(self.quizzes)

    def setIndexToRandomQuiz(self) -> None:
        self.currentQuizID = random.choice(self.quizzes)