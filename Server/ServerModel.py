import threading
import selectors
import time
import socket
import json
import os

import Server.GameModel as GameModel
import Server.ClientModel as ClientModel

class ServerModel:
    def __init__(self):
        self.listeningSocket = None
        self.selector = None
        self.rules = self.getStoredServerInformation()
        self.game = None
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

    def run(self):
        self.createListeningSocketAndSelector()

        self.isRunning = True