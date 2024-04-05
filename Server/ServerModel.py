import threading
import selectors
import time
import sys
import socket
import json
import os

from Response import Response
from ResponseStatusCode import ResponseStatusCode
from GameModel import GameModel
from ParticipantModel import ParticipantModel
from Request import Request
from RequestStatusCode import RequestStatusCode

class ServerModel:

    def __init__(self):
        self.listeningSocket = None
        self.selector = None
        self.rules = self.getStoredServerInformation()
        self.game = GameModel()
        self.isRunning = False

    @staticmethod
    def getStoredServerInformation():
        if not os.path.exists("./Data/server_information.json"):
            return {
                "host": "127.0.0.1",
                "port": 12000,
                "server_name": "localhost",
                "header": 64,
                "format": "utf-8"
            }
        
        with open("./Data/server_information.json", "r") as file:
            return json.load(file)

    def createListeningSocketAndSelector(self) -> bool:

        if self.rules is None:
            return False

        self.listeningSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        self.listeningSocket.setblocking(False)
        self.listeningSocket.bind((self.rules["host"], self.rules["port"]))
        self.listeningSocket.listen()

        self.selector = selectors.DefaultSelector()
        self.selector.register(self.listeningSocket, selectors.EVENT_READ, data=None)

        return True

    def closeConnections(self):
        self.listeningSocket.close()
        self.selector.unregister(self.listeningSocket)



        self.selector.close()

    def handleConnectionRequest(self, key, mask):

        connection, address = key.fileobj.accept()
        
        print(f"[SERVER] New connection request from {address}")

        if self.game.haveEnoughPlayers():
            watcher = ParticipantModel(connection, address)
            watcher.becomeWatcher()

            watcher.addResponse(Response(
                statusCode=ResponseStatusCode.GAME_FULL,
                content="Sorry, the game is full. You can only watch the game"
            ))

            self.game.addWatcher(watcher)

            self.selector.register(connection, selectors.EVENT_READ | selectors.EVENT_WRITE, data = watcher)
            
            print(f"[SERVER] New watcher with address {address} has joined the game")

            return
        
        player = ParticipantModel(connection, address)

        self.game.addPlayer(player)

        self.selector.register(connection, selectors.EVENT_READ | selectors.EVENT_WRITE, data = player)

        self.game.broadcastResponse(Response(
            statusCode=ResponseStatusCode.BROADCASTED_MESSAGE,
            content=f"Player with address {player.address} has joined the game"
        ))

        print(f"[SERVER] New player with address {address} has joined the game")

        player.addResponse(Response(
            statusCode=ResponseStatusCode.NICKNAME_REQUIREMENT,
            content="You need a nickname to continue the game"
        ))

    def handleNicknameRequest(self, participant : ParticipantModel, nickname : str) -> bool:
        if not ParticipantModel.checkNicknameValid(nickname):
            participant.addResponse(Response(
                statusCode=ResponseStatusCode.INVALID_NICKNAME,
                content="Invalid nickname. Please try again"
            ))
            print(f"[SERVER] Player with address {participant.address} has entered an invalid nickname ({nickname})")
            return False

        if self.game.playerList.checkNicknameExist(nickname):
            participant.addResponse(Response(
                statusCode=ResponseStatusCode.NICKNAME_ALREADY_TAKEN,
                content="Nickname already taken. Please try again"
            ))
            print(f"[SERVER] Player with address {participant.address} has entered a nickname ({nickname}) that is already taken")
            return False
                        
        participant.setNickname(nickname)
        participant.addResponse(Response(
            statusCode=ResponseStatusCode.NICKNAME_ACCEPTED,
            content="Nickname accepted. Please wait the game to start"
        ))

        self.game.broadcastResponse(Response(
            statusCode=ResponseStatusCode.BROADCASTED_MESSAGE,
            content=f"Player with address {participant.address} has set the nickname as {nickname}"
        ))

        print(f"[SERVER] Player with address {participant.address} has set the nickname as {nickname}")

        return True

    def serveConnection(self, key, mask):
        participantSocket = key.fileobj
        participant = key.data

        if (mask & selectors.EVENT_READ):
            receivedData = participantSocket.recv(1024)

            if receivedData:
                request = Request.getDeserializedRequest(receivedData.decode(self.rules["format"]))

                if request.getStatusCode() == RequestStatusCode.NICKNAME_REQUEST:
                    
                    self.handleNicknameRequest(
                        participant = participant, 
                        nickname = request.getContent()
                    )

                    


        if (mask & selectors.EVENT_WRITE):
            participant.sendMessageWithGivenSocket(participantSocket)

    def listen(self):

        while self.isRunning:

            events = self.selector.select(timeout=None)

            for key, mask in events:
                if key.data is None:
                    self.handleConnectionRequest(key, mask)   
                else:
                    self.serveConnection(key, mask)

    def run(self):

        self.isRunning = True

        while True:

            N = 0

            while True:
                N = int(input("Enter the number of players (between 2 and 10): "))
                if (N < 2) or (N > 10):
                    print("Invalid number of players. Please try again.")            
                else:
                    break

            self.createListeningSocketAndSelector()

            self.game.setPlayerCountRequirement(N)

            listeningThread = threading.Thread(target = self.listen)
        
            listeningThread.start()

            

            listeningThread.join()

            self.closeConnections()

            N = input("Do you want to start the another game? Please type 'Yes' in any case if you want to start the another game: ")
            if N.lower() != "yes":
                print("See you later")
                break

        self.isRunning = False