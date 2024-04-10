import threading
import socket
import json
import re
import sys

sys.path.append("../")
sys.path.append("./Message/")

from Request import Request
from RequestStatusCode import RequestStatusCode
from Response import Response
from ResponseStatusCode import ResponseStatusCode

class ClientModel:

    def __init__(self):
        self.clientSocket = None
        self.nickname = None
        self.summary = None
        
    def connectToServer(self, host : str, port : int) -> None:
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.connect((host, port))

    def sendRequest(self, request : Request) -> None:
        self.clientSocket.send(request.toString().encode())
