import sys
import random
import json
import os

from ParticipantModel import ParticipantModel

class PlayerList:

    def __init__(self):
        self.players = []
        self.countAlivePlayers = 0

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
    
    def findPlayerWithGivenNickanme(self, nickname : str):
        for player in self.players:
            if player.getNickname() == nickname:
                return player
        return None
    
    def checkNicknameExist(self, nickname : str) -> bool:
        return self.findPlayerWithGivenNickanme(nickname) is not None