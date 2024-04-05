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

    # def handleAnIteration(self):
    #     message = self.client.recv(1024).decode()
    #     if message == "Please enter your nickname: ":
    #         nickname = input(message)
    #         self.client.send(nickname.encode())
    #         return

    def listen(self):
        while True:
            receivedData = self.clientSocket.recv(1024).decode()
            
            if receivedData:
                response = Response.getDeserializedResponse(receivedData)

                if response.getStatusCode() == ResponseStatusCode.NICKNAME_ACCEPTED:
                    print(response.getContent())

                nickname = None
                
                if response.getStatusCode() == ResponseStatusCode.NICKNAME_REQUIREMENT:
                    nickname = input("Please enter your nickname: ")
                elif response.getStatusCode() == ResponseStatusCode.INVALID_NICKNAME:
                    nickname = input("The chosen nickname is not valid. Please enter a valid nickname: ")
                elif response.getStatusCode() == ResponseStatusCode.NICKNAME_ALREADY_TAKEN:
                    nickname = input("The chosen nickname is already taken. Please enter another nickname: ")
                
                if nickname is not None:
                    self.clientSocket.send(Request(
                        statusCode = RequestStatusCode.NICKNAME_REQUEST, 
                        content = nickname
                    ).toString().encode())

                if response.getStatusCode() == ResponseStatusCode.BROADCASTED_MESSAGE:
                    print(response.getContent())

    def run(self):
        
        listeningThread = threading.Thread(target = self.listen)
        
        listeningThread.start()

            

        listeningThread.join()
    
    def registration(self):
        raise NotImplementedError
    
    def submitAnswer(self):
        raise NotImplementedError
    
    def submitRegistration(self):
        raise NotImplementedError
    
    def submitDisconnect(self):
        raise NotImplementedError
    
    def updateCountDown(self):
        raise NotImplementedError
    
    def displayQuiz(self):
        raise NotImplementedError
    
    def displayDashboard(self):
        raise NotImplementedError
    
    def displaySummary(self):
        raise NotImplementedError
    
    
