import sys
import random
import json
import os

import sys
sys.path.append("./Quizzes/")
sys.path.append("./Message/")
sys.path.append("./Participants/")

from Quiz import Quiz
from QuizList import QuizList
from Response import Response
from PlayerList import PlayerList
from GameStatus import GameStatus
from ParticipantModel import ParticipantModel
from ResponseStatusCode import ResponseStatusCode

class GameModel:
    
    def __init__(self) -> None:
        self.quizList = QuizList()
        self.roundCount = 0
        self.players = PlayerList()
        self.watchers = []
        self.timeout = 20
        self.status = GameStatus.OFF
        self.guessedCharacters = []

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
        self.sendBroadcastedSummary()

    def addWatcher(self, watcher: ParticipantModel) -> None:
        self.watchers.append(watcher)
        self.sendBroadcastedSummary()

    def ready(self) -> None:
        self.roundCount = 0
        self.status = GameStatus.READY
        self.quizList.chooseRandomQuiz()

    def getClientCountSummary(self) -> dict:
        return {
            "required_number_of_players": self.rules["required_number_of_players"],
            "player_count": len(self.players),
            "successfully_registered_player_count": self.players.countSuccessfullyRegisteredPlayers(),
            "watcher_count": len(self.watchers)
        }

    def startNewMatch(self) -> bool:

        if self.players.countSuccessfullyRegisteredPlayers() < self.rules["required_number_of_players"]:
            return False

        self.status = GameStatus.RUNNING

        self.sendBroadcastedSummary()
            
        self.broadcastSummary()
        
        self.requireCurrentPlayerAnswer()
    
        self.broadcastResponse(Response(
            statusCode = ResponseStatusCode.GAME_STARTED,
            content = "Game started!!!"
        ))
    
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
    
    def getJSONSummary(self) -> dict:
        result = {
            "round_count": self.roundCount,
            "player": self.players.getJSONSummary(),
            "quiz": self.quizList.getJSONSummary(),
            "guessed_characters": self.guessedCharacters,
            "client_count_summary": self.getClientCountSummary()
        }

        return result
    
    def sendBroadcastedSummary(self) -> None:
        self.broadcastResponse(Response(
            statusCode = ResponseStatusCode.BROADCASTED_SUMMARY,
            content = json.dumps(self.getJSONSummary())
        ))
    
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
    
    def end(self) -> None:
        self.broadcastFinalResult()
        self.status = GameStatus.ENDED
        self.broadcastResponse(Response(
            statusCode = ResponseStatusCode.GAME_ENDED,
            content = "Game ended!!!"
        ))

    def stop(self) -> None:
        self.status = GameStatus.OFF
        self.players.clear()
        self.watchers.clear()
        self.guessedCharacters.clear()

    def moveTurnToNextPlayer(self) -> bool:
        #Return True if the game is still on, False otherwise
        if self.players.moveTurnToNextPlayer():
            self.roundCount += 1
            if self.roundCount >= 5:
                self.end()
                return False
        return self.status.isRunning()
        
    def handleAnswerSubmission(self, answer: dict) -> bool:
        if not self.status.isRunning():
            return True
        
        guessedCharacter = answer["guessed_character"]
        guessedKeyword = answer["guessed_keyword"]

        if guessedCharacter not in self.guessedCharacters:
            self.guessedCharacters.append(guessedCharacter)

        currentPlayer = self.players.getCurrentPlayer()
        quiz = self.quizList.getCurrentQuiz()

        flag = False

        if quiz.receiveLetterGuess(guessedCharacter):
            currentPlayer.score += self.rules["number_of_points_granted_for_correct_guess"]
            self.broadcastResponse(Response(
                statusCode = ResponseStatusCode.BROADCASTED_MESSAGE,
                content = f"Character '{guessedCharacter}' has {quiz.countOccernerces(guessedCharacter)} occurences in the keyword!!!"
            ))
        else:
            self.broadcastResponse(Response(
                statusCode = ResponseStatusCode.BROADCASTED_MESSAGE,
                content = f"Character '{guessedCharacter}' is not in the keyword!!!"
            ))
            flag = True

        if guessedKeyword is not None:
            if quiz.receiveKeywordGuess(guessedKeyword):
                currentPlayer.score += self.rules["number_of_points_granted_for_correct_keyword"]
                self.broadcastResponse(Response(
                    statusCode = ResponseStatusCode.BROADCASTED_MESSAGE,
                    content = f"{currentPlayer.getNickname()} has guessed the keyword!!!"
                ))
            else:

                self.broadcastResponse(Response(
                    statusCode = ResponseStatusCode.BROADCASTED_MESSAGE,
                    content = f"{currentPlayer.getNickname()} has guessed the wrong keyword!!!"
                ))

                if not self.players.disqualifyCurrentPlayer():
                    self.end()
                    
                    #self.broadcastResponse(Response(
                    #    statusCode = ResponseStatusCode.BROADCASTED_PLAYER_ANSWER,
                    #    content = json.dumps({
                    #        "guessed_character": guessedCharacter,
                    #        "guessed_keyword": guessedKeyword,
                    #        "author_nickname": currentPlayer.getNickname(),
                    #        "assessment": "The player is disqualified because of the wrong keyword guess!!!"
                    #    })
                    #))
                    
                    return True

                flag = True

        if quiz.isSolved():
            self.end()

            #self.broadcastResponse(Response(
            #    statusCode = ResponseStatusCode.BROADCASTED_PLAYER_ANSWER,
            #    content = json.dumps({
            #        "guessed_character": guessedCharacter,
            #        "guessed_keyword": guessedKeyword,
            #        "author_nickname": currentPlayer.getNickname(),
            #        "assessment": "The player has solved the quiz!!!"
            #        })
            #    ))

            return True
            
        if flag:
            if not self.moveTurnToNextPlayer():

                #self.broadcastResponse(Response(
                #    statusCode = ResponseStatusCode.BROADCASTED_PLAYER_ANSWER,
                #    content = json.dumps({
                #        "guessed_character": guessedCharacter,
                #        "guessed_keyword": guessedKeyword,
                #        "author_nickname": currentPlayer.getNickname(),
                #        "assessment": "The player has guessed wrong letter!!!"
                #    })
                #))

                return True
        
        self.broadcastSummary()
        self.sendBroadcastedSummary()

        self.requireCurrentPlayerAnswer()

        return False
    
    def getStatus(self) -> GameStatus:
        return self.status
    
    def broadcastFinalResult(self) -> None:
      
        self.broadcastResponse(Response(
            statusCode = ResponseStatusCode.BROADCASTED_MESSAGE,
            content = self.players.getRankSummary()
        ))

    def containsUnsentResponse(self) -> bool:
   
        for watcher in self.watchers:
            if watcher.containsUnsentResponse():
                return True
    
        for player in self.players:
            if player.containsUnsentResponse():
                return True
            
        return False