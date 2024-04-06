import threading
import socket

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
        
    def connectToServer(self, host : str, port : int) -> None:
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.connect((host, port))

    def sendRequest(self, request : Request) -> None:
        self.clientSocket.send(request.toString().encode())

    def listen(self):
        while True:
            receivedData = self.clientSocket.recv(1024).decode()
            
            if receivedData:
                response = Response.getDeserializedResponse(receivedData)

                statusCode = response.getStatusCode()
                content = response.getContent()

                if statusCode == ResponseStatusCode.NICKNAME_ACCEPTED:
                    print(content)

                nickname = None
                
                if statusCode == ResponseStatusCode.NICKNAME_REQUIREMENT:
                    nickname = input("Please enter your nickname: ")
                elif statusCode == ResponseStatusCode.INVALID_NICKNAME:
                    nickname = input("The chosen nickname is not valid. Please enter a valid nickname: ")
                elif statusCode == ResponseStatusCode.NICKNAME_ALREADY_TAKEN:
                    nickname = input("The chosen nickname is already taken. Please enter another nickname: ")
                
                if nickname is not None:
                    self.sendRequest(Request(
                        statusCode = RequestStatusCode.NICKNAME_REQUEST, 
                        content = nickname
                    ))

                if statusCode == ResponseStatusCode.BROADCASTED_MESSAGE:
                    print(content)

                if statusCode == ResponseStatusCode.ANSWER_REQUIRED:
                    answer = input(content)
                    self.sendRequest(Request(
                        statusCode = RequestStatusCode.ANSWER_SUBMISSION,
                        content = answer
                    ))

    def run(self):
        
        listeningThread = threading.Thread(target = self.listen)
        
        listeningThread.start()

            

        listeningThread.join()