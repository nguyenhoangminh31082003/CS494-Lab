import threading
import selectors
import time
import socket
import json
import os

import sys
sys.path.append("../")

import Server.GameModel as GameModel
import Server.ClientModel as ClientModel

class Server:
    def __init__(self, totalClient = 2):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.rules = Server.getRuleJSON()
        self.game = GameModel.GameModel()
        self.isRunning = True

    @staticmethod
    def getRuleJSON():
        if not os.path.exists("./Data/rules.json"):
            return {
                "maximum_client_count": 10,
                "host": "127.0.0.1",
                "port": 12000,
                "server_name": "localhost",
                "header": 64,
                "format": "utf-8"
            }
        
        with open("./Data/rules.json", "r") as file:
            return json.load(file)

    def receiveClientRequestForConnection(self):
        while len(self.clients) < self.rules["maximum_client_count"]:
            print("[SERVER] Waiting for connection...")
            connection, address = self.server.accept()
            
            self.game.appendClient(ClientModel.ClientModel(connection, address))
            print("[SERVER] Connection from", address)
            thread = threading.Thread(target=self.handleRegistration, args=(connection, address))
            thread.start()
            
    # def askForNickname(self, index: int, connection):
    #     connection.send("Please enter your nickname: ".encode())
    #     nickname = connection.recv(1024).decode()
    #     return nickname

    def handleRegistration(self, connection, address):
        index = self.game.getClientIndex(address)
        raise NotImplementedError
        
        # if self.players[index].getNickname() is None:
        #     connection.send("Please enter your nickname: ".encode())
        #     nickname = connection.recv(1024).decode()
        #     if not self.players[index].setNickname(nickname):
        #         connection.send("Invalid nickname. Please try again.".encode())
        #         connection.close()
        #         return
        
    def run(self):
        self.receiveClientRequestForConnection()
        self.isRunning = True
        while self.isRunning:
            # input Y/N to start a new game
            state = input("Start a new game? (Y/N): ")
            if state == "N":
                self.isRunning = False
                break
            # start a new game
            self.game.startNewGame()
            raise NotImplementedError
        self.server.close()
        