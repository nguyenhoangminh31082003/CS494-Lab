import sys
import random
import json
import os

from ParticipantModel import ParticipantModel

class PlayerList:

    def __init__(self):
        self.players = []
        self.countAlivePlayers = 0
        self.currentID = 0

    def getCurrentPlayer(self):
        if (0 <= self.currentID) and (self.currentID < len(self.players)):
            return self.players[self.currentID]
        return None

    def __getitem__(self, key : int) -> ParticipantModel:   
        return self.players[key]
    
    def __setitem__(self, key : int, value : ParticipantModel) -> None:
        self.players[key] = value
    
    def __len__(self) -> int:
        return len(self.players)
    
    def __iter__(self):
        return iter(self.players)
    
    def addPlayer(self, player : ParticipantModel) -> None:
        self.players.append(player)
        if player.isAlive():
            self.countAlivePlayers += 1

    def countAlivePlayers(self) -> int:
        return self.countAlivePlayers
    
    def findPlayerPosition(self, nickname : str) -> int:
        for i, player in enumerate(self.players):
            if player.getNickname() == nickname:
                return i
        return -1
    
    def checkNicknameExist(self, nickname : str) -> bool:
        return self.findPlayerPosition(nickname) >= 0

    def getFormattedSummary(self) -> str:
        resultLines = [
            f"Current player: {self.players[self.currentID].getNickname()}",
            f"{"order".rjust(10)}| {"nickname".rjust(10)}| {"points".rjust(10)}"
        ]
        
        for i, player in enumerate(self.players):
            resultLines.append(f"{str(i).rjust(10)}| {player.getNickname().rjust(10)}| {str(player.score).rjust(10)}")

        return "\n".join(resultLines)
    
    def countSuccessfullyRegisteredPlayers(self) -> int:
        return len([player for player in self.players if player.getNickname() is not None])
    
    def moveTurnToNextPlayer(self) -> None:
        playerCount = len(self.players)

        self.currentID = (self.currentID + 1) % playerCount
        while not self.players[self.currentID].isAlive():
            self.currentID = (self.currentID + 1) % playerCount

    def disqualifyCurrentPlayer(self) -> bool:
        currentPlayer = self.getCurrentPlayer()

        currentPlayer.die()

        self.countAlivePlayers -= 1

        if self.countAlivePlayers >= 1
            self.moveTurnToNextPlayer()
            return True
        
        return False