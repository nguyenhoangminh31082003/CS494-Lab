import sys
import random
sys.path.append("../")
from Server.ClientModel import ClientModel

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

class GameModel:
    def __init__(self) -> None:
        self.quizzes = []
        self.readQuizzes()
        self.round = 0
        self.people = []
        self.alive_players = 0
        self.current_player = 0
        self.current_quiz = None
        self.timeout = 20
        self.is_game_on = False
        
    def readQuizzes(self) -> None:
        with open("data.txt", "r") as file:
            number_of_words = int(file.readline())
            for _ in range(number_of_words):
                tmp = file.readline().split(":")
                self.quizzes.append(Quiz(tmp[0], tmp[1]))
    
    def chooseQuiz(self) -> None:
        self.current_quiz = random.choice(self.quizzes)
    
    def addPlayer(self, player: ClientModel) -> None:
        self.people.append(player)
        alive_players += 1
    
    def handleGuess(self, guess: str, is_final_guess: bool) -> None:
        if is_final_guess:
            if self.current_quiz.guessKeyword(guess):
                self.people[self.current_player].correctAnswerKeyword()
            else:
                self.findNextPlayer()
        else:
            if self.current_quiz.guessLetter(guess):
                self.people[self.current_player].correctAnswerLetter()
            else:
                self.people[self.current_player].wrongAnswerKeyword()
                self.alive_players -= 1
                self.findNextPlayer()
            
    def findNextPlayer(self) -> None:
        # next player with mode PLAY in "people"
        raise NotImplementedError
    
    def getClientIndex(self, address) -> int:
        # find player in "people" by address and return the index
        raise NotImplementedError 
    
    def summary(self) -> None:
        # print only player with mode DIE and PLAY
        self.is_game_on = False
        raise NotImplementedError
    
    def startNewGame(self) -> None:
        alive_players = len(self.people)
        self.round = 0
        self.chooseQuiz()
        self.current_player = 0
        for i in range(alive_players):
            self.people[i].reset()
        self.is_game_on = True
            