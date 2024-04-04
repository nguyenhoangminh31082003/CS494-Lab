import threading
import selectors
import time
import socket
import json
import os

from Server.GameModel import GameModel
from Server.ParticipantModel import ParticipantModel

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
        
        if self.game.haveEnoughPlayers():
            #connection.sendall("Sorry, the game is full. You can only watch the game".encode(self.rules["format"]))
            watcher = ParticipantModel(connection, address)
            watcher.becomeWatcher()

            watcher.addMessageToBeSent("Sorry, the game is full. You can only watch the game")

            self.game.addWatcher(watcher)

            self.selector.register(connection, selectors.EVENT_READ | selectors.EVENT_WRITE, data = watcher)
            return
        
        player = ParticipantModel(connection, address)

        self.game.addPlayer(player)

        self.selector.register(connection, selectors.EVENT_READ | selectors.EVENT_WRITE, data = player)

        self.game.broadcastMessage(f"Player with address {player.address} has joined the game")

    def serveConnection(self, key, mask):
        participantSocket = key.fileobj
        participant = key.data

        if (mask & selectors.EVENT_READ):
            receivedData = participantSocket.recv(1024)

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
                    pass

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



            N = input("Do you want to start the another game? Please type 'Yes' in any case if you want to start the another game: ")
            if N.lower() != "yes":
                print("See you later")
                break

        self.isRunning = False