import threading
import selectors
import socket
import json
import time
import sys
import os

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
    def getStoredServerInformation() -> dict:
        fileName = "./Data/server_information.json"

        if not os.path.exists(fileName):
            return {
                "host": "127.0.0.1",
                "port": 12000,
                "server_name": "localhost",
                "header": 64,
                "format": "utf-8"
            }
        
        with open(fileName, "r") as file:
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

            self.game.addWatcher(watcher)

            watcher.addResponse(Response(
                statusCode = ResponseStatusCode.GAME_FULL,
                content = json.dumps({
                    "message": "The game is full. You can only watch the game.",
                    "game_started": self.game.getStatus().isRunning()
                })
            ))

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
        
    def handleCloseConnectionRequest(self, participant : ParticipantModel, participantSocket : socket.socket) -> None:
        participantSocket.close()
        self.selector.unregister(participantSocket)
        content = ""
        
        if participant.getNickname() is None:
            self.game.removeUnregisteredPlayer(participant)
            content = f"Client with address {participant.address} has left the game"
            
        elif participant.isWatcher():
            self.game.removeWatcher(participant)
            self.game.removeUnregisteredPlayer(participant)
            content = f"Watcher with address {participant.address} has left the game"
        
        elif participant.isWaiting():
            content = f"Waiting with address {participant.address} has left the game"
            self.game.removeUnregisteredPlayer(participant)
        else:
            content = f"Player with address {participant.address} has left the game"
            self.game.removeRegisteredPlayer(participant)

        print(f"[SERVER] {content}")
        
        self.game.broadcastResponse(Response(
            statusCode=ResponseStatusCode.BROADCASTED_MESSAGE,
            content=content
        ))

        if self.game.countPlayers() > 0:
            self.game.sendBroadcastedSummary()
            
        ## handle the case when no player is left

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

        self.game.sendBroadcastedSummary()

        print(f"[SERVER] Player with address {participant.address} has set the nickname as {nickname}")

        self.game.startNewMatch()

        return True
    
    def handleRestartRequest(self, participant : ParticipantModel) -> bool:
        
        nickname = participant.getNickname()

        if not self.game.reallowPlayerWithNickname(nickname):
            return False

        participant.addResponse(Response(
            statusCode=ResponseStatusCode.WAIT_GAME_START_REQUIRED,
            content= f"Registration Completed Successfully. You will have {self.game.findPlayerPosition(nickname)}-th turn in the game"
        ))

        return self.game.startNewMatch()

    def serveConnection(self, key, mask):
        participantSocket = key.fileobj
        participant = key.data

        if (mask & selectors.EVENT_READ):
            receivedData = participantSocket.recv(1024)

            if receivedData:
                receivedData = receivedData.decode().strip()

                print(f"[SERVER] Received data: {receivedData}")

                request = Request.getDeserializedRequest(receivedData)

                statusCode = request.getStatusCode()
                content = request.getContent()
                
                if statusCode == RequestStatusCode.CLOSE_CONNECTION:
                    self.handleCloseConnectionRequest(participant, participantSocket)

                elif statusCode == RequestStatusCode.NICKNAME_REQUEST:
                    
                    self.handleNicknameRequest(
                        participant = participant, 
                        nickname = request.getContent()
                    )

                elif statusCode == RequestStatusCode.ANSWER_SUBMISSION:
                    self.game.handleAnswerSubmission(json.loads(content))

                elif statusCode == RequestStatusCode.RESTART_NEW_MATCH:
                    self.handleRestartRequest(participant)

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

            if self.game.getStatus().isEnded() and (not self.game.containsUnsentResponse()):
                while True:
                    administratorAnswer = input("Do you want to restart the game? (yes/no): ").lower()
                    if administratorAnswer == "yes":
                        self.game.prepareForRestart()
                        break
                    elif administratorAnswer == "no":
                        self.game.stop()
                        break
                    else:
                        print("Invalid answer. Please try again.")

            if self.game.getStatus().isRunning():
                self.game.handleTimer()

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

        N = self.readPlayerCountRequirement()

        self.createListeningSocketAndSelector()

        self.game.setPlayerCountRequirement(N)

        while True:

            self.game.ready()

            listeningThread = threading.Thread(target = self.listen)
        
            listeningThread.start()

            print(f"[SERVER] Server is running on {self.rules['host']}:{self.rules['port']} and starts listening")

            listeningThread.join()

            self.closeConnections()

        self.isRunning = False