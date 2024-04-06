import threading
import selectors
import time
import sys
import socket
import json
import os

import sys
sys.path.append("./Message/")
sys.path.append("./Participants/")
sys.path.append("./Game/")

from Request import Request
from Response import Response
from GameModel import GameModel
from GameStatus import GameStatus
from ParticipantModel import ParticipantModel
from RequestStatusCode import RequestStatusCode
from ResponseStatusCode import ResponseStatusCode


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

    def startGame(self):
        if self.game.startNewGame():
            self.game.broadcastSummary()
            self.game.requireCurrentPlayerAnswer()

    def handleNicknameRequest(self, participant : ParticipantModel, nickname : str) -> bool:
        if not ParticipantModel.checkNicknameValid(nickname):
            participant.addResponse(Response(
                statusCode=ResponseStatusCode.INVALID_NICKNAME,
                content="Invalid nickname. Please try again"
            ))
            print(f"[SERVER] Player with address {participant.address} has entered an invalid nickname ({nickname})")
            return False

        if self.game.containsPlayer(nickname):
            participant.addResponse(Response(
                statusCode=ResponseStatusCode.NICKNAME_ALREADY_TAKEN,
                content="Nickname already taken. Please try again"
            ))
            print(f"[SERVER] Player with address {participant.address} has entered a nickname ({nickname}) that is already taken")
            return False
                        
        participant.setNickname(nickname)

        participant.addResponse(Response(
            statusCode=ResponseStatusCode.NICKNAME_ACCEPTED,
            content= f"Registration Completed Successfully. You will have {self.game.findPlayerPosition(nickname)}-th turn in the game"
        ))

        self.game.broadcastResponse(Response(
            statusCode=ResponseStatusCode.BROADCASTED_MESSAGE,
            content=f"Player with address {participant.address} has set the nickname as {nickname}"
        ))

        print(f"[SERVER] Player with address {participant.address} has set the nickname as {nickname}")

        self.startGame()

        return True

    def serveConnection(self, key, mask):
        participantSocket = key.fileobj
        participant = key.data

        if (mask & selectors.EVENT_READ):
            receivedData = participantSocket.recv(1024)

            if receivedData:
                request = Request.getDeserializedRequest(receivedData.decode(self.rules["format"]))

                statusCode = request.getStatusCode()
                content = request.getContent()

                if statusCode == RequestStatusCode.NICKNAME_REQUEST:
                    
                    self.handleNicknameRequest(
                        participant = participant, 
                        nickname = request.getContent()
                    )

                elif statusCode == RequestStatusCode.ANSWER_SUBMISSION:
                    self.game.handleAnswerSubmission(json.loads(content))

        if (mask & selectors.EVENT_WRITE):
            participant.sendResponse(participantSocket)

    def listen(self):

        while self.game.getStatus().isNotOff():

            events = self.selector.select(timeout=None)

            for key, mask in events:
                if key.data is None:
                    self.handleConnectionRequest(key, mask)   
                else:
                    self.serveConnection(key, mask)

    def readPlayerCountRequirement(self) -> int:
        N = 0

        while True:
            N = int(input("Enter the number of players (between 2 and 10): "))
            if (N < 2) or (N > 10):
                print("Invalid number of players. Please try again.")            
            else:
                break

        return N

    def run(self):

        self.isRunning = True

        while True:

            N = self.readPlayerCountRequirement()

            self.createListeningSocketAndSelector()

            self.game.setPlayerCountRequirement(N)

            self.game.ready()

            listeningThread = threading.Thread(target = self.listen)
        
            listeningThread.start()

            print(f"[SERVER] Server is running on {self.rules['host']}:{self.rules['port']} and starts listening")

            listeningThread.join()

            self.closeConnections()

            N = input("Do you want to start the another game? Please type 'Yes' in any case if you want to start the another game: ").lower()
            if N != "yes":
                print("See you later")
                break

        self.isRunning = False