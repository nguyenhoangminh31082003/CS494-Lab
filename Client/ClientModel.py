import threading
import socket

import sys
sys.path.append("../")

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

    def run(self):
        #thread = threading.Thread(target=self.handleAnIteration)
        #thread.start()
        pass
    
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
    
    
