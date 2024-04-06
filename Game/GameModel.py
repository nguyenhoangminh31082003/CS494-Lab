import sys
import random
import json
import os

import sys
sys.path.append("./Quizzes/")
sys.path.append("./Message/")
sys.path.append("./Participants/")

from ParticipantModel import ParticipantModel
from Quiz import Quiz
from QuizList import QuizList
from Response import Response
from ResponseStatusCode import ResponseStatusCode
from PlayerList import PlayerList
from GameStatus import GameStatus

class GameModel:
    
    def __init__(self) -> None:
        self.quizList = QuizList()
        self.roundCount = 0
        self.players = PlayerList()
        self.watchers = []
        self.timeout = 20
        self.status = GameStatus.OFF

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

    def ready(self) -> None:
        self.roundCount = 0
        self.status = GameStatus.READY
        self.quizList.chooseRandomQuiz()

    def startNewGame(self) -> bool:

        if self.players.countSuccessfullyRegisteredPlayers() < self.rules["required_number_of_players"]:
            return False

        self.status = GameStatus.RUNNING
    
        return True

    def getRoundCount(self) -> int:
        return self.roundCount
    
    def broadcastResponse(self, message: Response) -> None:
        for player in self.players:
            player.addResponse(message)
        for watcher in self.watchers:
            watcher.addResponse(message)

    def containsPlayer(self, nickname: str) -> bool:
        return self.players.checkNicknameExist(nickname)
    
    def findPlayerPosition(self, nickname: str) -> int:
        return self.players.findPlayerPosition(nickname)
    
    def getSummary(self) -> str:
        return "\n".join([
            f"Number of rounds: {self.roundCount}",
            self.players.getFormattedSummary(),
            self.quizList.getFormattedSummary()
        ])
    
    def broadcastSummary(self) -> None:
        self.broadcastResponse(Response(
            statusCode = ResponseStatusCode.BROADCASTED_MESSAGE,
            content = self.getSummary()
        ))

    def broadcastQuestion(self) -> None:
        self.broadcastResponse(Response(
            statusCode = ResponseStatusCode.QUESTION_SENT,
            content = self.quizList.getSerializedQuestion()
        ))

    def requireCurrentPlayerAnswer(self) -> None:
        self.players.getCurrentPlayer().addResponse(Response(
            statusCode = ResponseStatusCode.ANSWER_REQUIRED,
            content = json.dumps({
                "keyword_guess_allowance": (self.roundCount >= 2)
            })
        ))

    def findWinner(self) -> ParticipantModel:
        result = i
        for i, player in enumerate(self.players):
            if self.players[result].score < player.score:
                result = i
        return self.players[result]
    
    def stopTheGame(self) -> None:
        self.status = GameStatus.OFF
        self.broadcastResponse(Response(
            statusCode = ResponseStatusCode.GAME_ENDED,
            content = "Game ended!!!"
        ))

    def moveTurnToNextPlayer(self) -> bool:
        #Return True if the game is still on, False otherwise
        if self.players.moveTurnToNextPlayer():
            self.roundCount += 1
            if self.roundCount >= 5:
                self.stopTheGame()
                return False
        return self.status.isRunning()
        
    def handleAnswerSubmission(self, answer: dict) -> bool:
        if not self.status.isRunning():
            return True
        
        guessedCharacter = answer["guessed_character"]
        guessedKeyword = answer["guessed_keyword"]

        currentPlayer = self.players.getCurrentPlayer()
        quiz = self.quizList.getCurrentQuiz()

        flag = False

        if quiz.receiveLetterGuess(guessedCharacter):
            currentPlayer.score += self.rules["number_of_points_granted_for_correct_guess"]
        else:
            flag = True

        if guessedKeyword is not None:
            if quiz.receiveKeywordGuess(guessedKeyword):
                currentPlayer.score += self.rules["number_of_points_granted_for_correct_keyword"]
            else:

                if not self.players.disqualifyCurrentPlayer():
                    self.stopTheGame()
                    return True

                flag = True

        if quiz.isSolved():
            self.stopTheGame()
            return True
            
        if flag:
            if not self.moveTurnToNextPlayer():
                return True
        
        self.broadcastSummary()

        self.requireCurrentPlayerAnswer()

        return False
    
    def getStatus(self) -> GameStatus:
        return self.status