import sys
import random
import json
import os

import sys
sys.path.append("./Quizzes/")

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
        self.timeout = 20
        self.isGameOn = False

        self.rules = self.getStoredGameInformation()

    def haveEnoughPlayers(self) -> bool:
        return len(self.players) >= self.rules["required_number_of_players"]

    def setPlayerCountRequirement(self, count: int) -> bool:
        if (count < 2) or (count > 10):
            return False
        self.rules["required_number_of_players"] = count
        self.saveGameInformation()
        return True
    
    def saveGameInformation(self) -> None:
        with open("./Data/game_information.json", "w") as file:
            json.dump(self.rules, file)
        
    @staticmethod
    def getStoredGameInformation():
        if not os.path.exists("./Data/game_information.json"):
            return {
                "required_number_of_players": 5,
                "number_of_points_granted_for_correct_guess": 1,
                "number_of_points_granted_for_correct_keyword": 5
            }
        
        with open("./Data/game_information.json", "r") as file:
            return json.load(file)
        
    def addPlayer(self, player: ParticipantModel) -> None:
        self.players.addPlayer(player)

    def addWatcher(self, watcher: ParticipantModel) -> None:
        self.watchers.append(watcher)
    
    def startNewGame(self) -> bool:

        if self.players.countSuccessfullyRegisteredPlayers() < self.rules["required_number_of_players"]:
            return False

        self.roundCount = 0
        self.isGameOn = True
        self.quizList.chooseRandomQuiz()
    
        return True

    def getRoundCount(self) -> int:
        return self.roundCount
    
    def checkGameOn(self) -> bool:
        return self.isGameOn
    
    def broadcastResponse(self, message: Response) -> None:
        for player in self.players:
            player.addResponse(message)
        for watcher in self.watchers:
            watcher.addResponse(message)

    def containsPlayer(self, nickname: str) -> bool:
        return self.players.checkNicknameExist(nickname)
    
    def findPlayerPosition(self, nickname: str) -> int:
        return self.players.findPlayerPosition(nickname)
    
    def getStartAnouncement(self) -> str:
        return self.players.getFormattedSummary() + "\n" + self.quizList.getFormattedSummary()