import sys
import random
import json
import os

from Server.ParticipantModel import ParticipantModel
from Server.Quiz import Quiz

class GameModel:
    
    def __init__(self) -> None:
        self.quizzes = []
        self.readQuizzes()
        self.roundCount = 0
        self.players = []
        self.watchers = []
        self.alivePlayerCount = 0
        self.currentPlayerID = 0
        self.currentQuizID = None
        self.timeout = 20
        self.isGameOn = False
        self.requiredPlayerCount = self.getStoredGameInformation()["required_number_of_players"]

    def haveEnoughPlayers(self) -> bool:
        return len(self.players) >= self.requiredPlayerCount

    def setPlayerCountRequirement(self, count: int) -> bool:
        if count < 2 or count > 10:
            return False
        self.requiredPlayerCount = count
        self.saveGameInformation()
        return True
        
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
            wordCount = int(file.readline())
            for _ in range(wordCount):
                tmp = file.readline().split(":")
                self.quizzes.append(Quiz(tmp[0], tmp[1]))
    
    def chooseQuiz(self) -> None:
        self.currentQuizID = random.choice(self.quizzes)
    
    def addPlayer(self, player: ParticipantModel) -> None:
        self.players.append(player)
        self.alivePlayerCount += 1

    def addWatcher(self, watcher: ParticipantModel) -> None:
        self.watchers.append(watcher)
    
    def handleGuess(self, guess: str, is_final_guess: bool) -> None:
        if is_final_guess:
            if self.currentQuizID.guessKeyword(guess):
                self.players[self.currentPlayerID].correctAnswerKeyword()
            else:
                self.findNextPlayer()
        else:
            if self.currentQuizID.guessLetter(guess):
                self.players[self.currentPlayerID].correctAnswerLetter()
            else:
                self.players[self.currentPlayerID].wrongAnswerKeyword()
                self.alivePlayerCount -= 1
                self.findNextPlayer()
            
    def findNextPlayer(self) -> None:
        # next player with mode PLAY in "players"
        raise NotImplementedError
    
    def getClientIndex(self, address) -> int:
        # find player in "players" by address and return the index
        raise NotImplementedError 
    
    def summary(self) -> None:
        # print only player with mode DIE and PLAY
        self.isGameOn = False
        raise NotImplementedError
    
    def startNewGame(self) -> None:
        alivePlayerCount = len(self.players)
        self.roundCount = 0
        self.chooseQuiz()
        self.currentPlayerID = 0
        for i in range(alivePlayerCount):
            self.players[i].reset()
        self.isGameOn = True
    
    def getRoundCount(self) -> int:
        return self.roundCount
    
    def checkGameOn(self) -> bool:
        return self.isGameOn
    
    def broadcastMessage(self, message: str) -> None:
        for player in self.players:
            player.addMessageToBeSent(message)
        for watcher in self.watchers:
            watcher.addMessageToBeSent(message)