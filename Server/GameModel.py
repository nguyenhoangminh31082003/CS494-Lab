import sys
import random
import json
import os

from ParticipantModel import ParticipantModel
from Quiz import Quiz
from QuizList import QuizList
from Response import Response
from ResponseStatusCode import ResponseStatusCode
from PlayerList import PlayerList

class GameModel:
    
    def __init__(self) -> None:
        self.quizList = QuizList()
        self.roundCount = 0
        self.players = PlayerList()
        self.watchers = []
        self.currentPlayerID = 0
        self.timeout = 20
        self.isGameOn = False
        self.requiredPlayerCount = self.getStoredGameInformation()["required_number_of_players"]

    def haveEnoughPlayers(self) -> bool:
        return len(self.players) >= self.requiredPlayerCount

    def setPlayerCountRequirement(self, count: int) -> bool:
        if (count < 2) or (count > 10):
            return False
        self.requiredPlayerCount = count
        self.saveGameInformation()
        return True
    
    def saveGameInformation(self) -> None:
        with open("./Data/game_information.json", "w") as file:
            json.dump({
                "required_number_of_players": self.requiredPlayerCount
            }, file)
        
    @staticmethod
    def getStoredGameInformation():
        if not os.path.exists("./Data/game_information.json"):
            return {
                "required_number_of_players": 10
            }
        
        with open("./Data/game_information.json", "r") as file:
            return json.load(file)
        
    def addPlayer(self, player: ParticipantModel) -> None:
        self.players.addPlayer(player)

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
        self.setIndexToRandomQuiz()
        self.currentPlayerID = 0
        for i in range(alivePlayerCount):
            self.players[i].reset()
        self.isGameOn = True
    
    def getRoundCount(self) -> int:
        return self.roundCount
    
    def checkGameOn(self) -> bool:
        return self.isGameOn
    
    def broadcastResponse(self, message: Response) -> None:
        for player in self.players:
            player.addResponse(message)
        for watcher in self.watchers:
            watcher.addResponse(message)

    def containsPlayerWithNickname(self, nickname: str) -> bool:
        return self.players.checkNicknameExist(nickname)