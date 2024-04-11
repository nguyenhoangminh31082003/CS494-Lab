import sys
import random
import json
import os

import sys
sys.path.append("./Participants/")

from ParticipantModel import ParticipantModel

class PlayerList:

    def __init__(self):
        self.players = []
        self.countAlivePlayers = 0
        self.currentID = 0

    def clear(self) -> None:
        self.players.clear()
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
        
    def removeRegisteredPlayer(self, nickname) -> None:
        position = self.findPlayerPosition(nickname)
        self.players[position].die()
        
    def removeUnregisteredPlayer(self, player : ParticipantModel) -> None:
        self.players.remove(player)

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
            f"{"Order".rjust(10)}| {"Nickname".rjust(10)}| {"Points".rjust(10)}| {"Alive".rjust(10)}"
        ]
        
        for i, player in enumerate(self.players):
            resultLines.append(f"{str(i).rjust(10)}| {player.getNickname().rjust(10)}| {str(player.score).rjust(10)}| {("Yes" if player.isAlive() else "No").rjust(10)}")

        return "\n".join(resultLines)
    
    def getJSONSummary(self) -> dict:
        result = {
            "current_player": self.players[self.currentID].getNickname(),
            "player_count": len(self.players),
            "player_information": []
        }

        for i, player in enumerate(self.players):
            result["player_information"].append({
                "order": i,
                "nickname": player.getNickname(),
                "points": player.score,
                "alive": player.isAlive()
            })

        return result

    def getRankSummary(self) -> str:
        winners = []
        playerCount = len(self.players)
        indices = list(range(playerCount))
        indices.sort(key = lambda x: self.players[x].score, reverse = True)
        points = -1
        rank = 0

        resultLines = [
            f"{"Rank".rjust(10)} | {"Order".rjust(10)}| {"Nickname".rjust(10)}| {"Points".rjust(10)}"
        ]

        for i, index in enumerate(indices):
            score = self.players[index].score
            if points != score:
                points = score
                rank = i + 1
            if rank == 1:
                winners.append(index)
            resultLines.append(f"{str(rank).rjust(10)} | {str(index).rjust(10)}| {self.players[index].getNickname().rjust(10)}| {str(points).rjust(10)}")

        if len(winners) == 1:
            resultLines.append(f"\n{self.players[winners[0]].getNickname()} is the winner!")
        else:
            resultLines.append(f"\nWinners are: {', '.join([self.players[winners[i]].getNickname() for i in range(len(winners))])}")

        return "\n".join(resultLines)
    
    def countSuccessfullyRegisteredPlayers(self) -> int:
        return len([player for player in self.players if player.getNickname() is not None])
    
    def moveTurnToNextPlayer(self) -> bool:
        playerCount = len(self.players)

        result = False

        while True:
            self.currentID += 1

            if self.currentID >= playerCount:
                self.currentID = 0
                result = True

            if self.players[self.currentID].isAlive():
                break

        return result

    def disqualifyCurrentPlayer(self) -> bool:
        currentPlayer = self.getCurrentPlayer()

        currentPlayer.die()

        self.countAlivePlayers -= 1
        
        return self.countAlivePlayers >= 1