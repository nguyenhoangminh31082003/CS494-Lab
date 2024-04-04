import sys
import random
import json
import os

from Server.ClientModel import ClientModel
from Server.Quiz import Quiz

class GameModel:
    
    def __init__(self) -> None:
        self.quizzes = []
        self.readQuizzes()
        self.round = 0
        self.people = []
        self.number_of_alive_players = 0
        self.current_player = 0
        self.current_quiz = None
        self.timeout = 20
        self.is_game_on = False
        
    @staticmethod
    def getStoredGameInformation(self):
        if not os.path.exists("./Data/game_information.json"):
            return {
                "required_number_of_players": 10
            }
        
        with open("./Data/game_information.json", "r") as file:
            return json.load(file)


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
        number_of_number_of_alive_players += 1
    
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
                self.number_of_alive_players -= 1
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
        number_of_alive_players = len(self.people)
        self.round = 0
        self.chooseQuiz()
        self.current_player = 0
        for i in range(number_of_alive_players):
            self.people[i].reset()
        self.is_game_on = True
            
    def run(self):
        pass
    