import threading
import socket
import queue
import json
import sys
import re

sys.path.append("../")
sys.path.append("./Message/")

from Request import Request
from Response import Response
from RequestStatusCode import RequestStatusCode
from ResponseStatusCode import ResponseStatusCode

class ClientModel:

    def __init__(self):
        self.clientSocket = None
        self.nickname = None
        self.receivedResponses = queue.Queue()  
        
    def connectToServer(self, host : str, port : int) -> None:
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.connect((host, port))

    def sendRequest(self, request : Request) -> None:
        self.clientSocket.send(request.toString().encode())

    def closeConnection(self):
        self.clientSocket.close()

    def requestNickname(self, nickname : str) -> None:
        self.sendRequest(Request(RequestStatusCode.NICKNAME_REQUEST, nickname))

    def listen(self):
        while True:
            receivedData = self.clientSocket.recv(1024).decode()
            
            if receivedData:
                self.receivedResponses.put(Response.getDeserializedResponse(receivedData))

    def getReceivedResponse(self):

        if not self.receivedResponses.empty():   
            return self.receivedResponses.get()
        
        return None