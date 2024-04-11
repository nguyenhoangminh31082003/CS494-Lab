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
        message = request.toString().encode("utf-8")

        length = len(message)

        message += b" " * (1024 - length)

        self.clientSocket.send(message)

        print(f"[CLIENT] Sent data: {request.toString()}")

    def closeConnection(self):
        self.requestCloseConnection()
        self.clientSocket.close()

    def requestNickname(self, nickname : str) -> None:
        self.sendRequest(Request(RequestStatusCode.NICKNAME_REQUEST, nickname))
        
    def sendLetterGuess(self, letter : str) -> None:
        self.sendRequest(Request(
        statusCode = RequestStatusCode.ANSWER_SUBMISSION,
            content = json.dumps({
                "guessed_character": letter,
                "guessed_keyword": None,
            })
        ))
    
    def sendWordGuess(self, word : str) -> None:
        self.sendRequest(Request(
        statusCode = RequestStatusCode.ANSWER_SUBMISSION,
            content = json.dumps({
                "guessed_keyword": word,
                "guessed_character": None,
            })
        ))
        
    def requestCloseConnection(self) -> None:
        self.sendRequest(Request(RequestStatusCode.CLOSE_CONNECTION, "Close connection"))

    def listen(self):
        while True:
            try:
                receivedData = self.clientSocket.recv(1024).decode().strip()
                
            except:
                break
            
            if receivedData:

                #print(f"[CLIENT] Received data: {receivedData}")

                self.receivedResponses.put(Response.getDeserializedResponse(receivedData))

    def getReceivedResponse(self):

        if not self.receivedResponses.empty():   

            response = self.receivedResponses.get()

            #print(f"!!![CLIENT] Returning response: {response.toString()}")

            return response 
        
        return None