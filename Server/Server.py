import threading
import socket
import json
import os

import sys
sys.path.append("../")

import Player

class Server:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        address = Server.getAddress()
        self.server.bind((address["host"], address["port"]))
        self.server.listen()
        print("[SERVER] Server is listening on", address)

        self.clients = []
        self.rules = Server.getRuleJSON()
        self.players = []
    

    @staticmethod
    def getRuleJSON():
        if not os.path.exists("./Data/rules.json"):
            return {
                "maximum_client_count": 10
            }
        
        with open("./Data/rules.json", "r") as file:
            return json.load(file)

    @staticmethod
    def getAddress():
        return {"host": "127.0.0.1", "port": "65432"}
    
    def receiveClientRequestForConnection(self):
        while len(self.clients) < self.rules["maximum_client_count"]:
            connection, address = self.server.accept()
            self.clients.append(connection)
            print("[SERVER] Connection from", address)
            thread = threading.Thread(target=self.handleClient, args=(connection, address))
            thread.start()
            self.players.append(Player())

    def handleClient(self, connection, address):
        pass