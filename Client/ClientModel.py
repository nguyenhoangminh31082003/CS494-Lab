import threading
import socket
import json

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

    def handleRegistration(self, statusCode: ResponseStatusCode, content: str) -> None:
        if statusCode == ResponseStatusCode.NICKNAME_ACCEPTED:
            print(content)
            return

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

    def listen(self):
        while True:
            receivedData = self.clientSocket.recv(1024).decode()
            
            if receivedData:
                response = Response.getDeserializedResponse(receivedData)

                statusCode = response.getStatusCode()
                content = response.getContent()

                if statusCode.isNicknameRelated():
                    self.handleRegistration(statusCode, content)        
                elif statusCode == ResponseStatusCode.BROADCASTED_MESSAGE:
                    print(content)
                elif statusCode == ResponseStatusCode.QUESTION_SENT:
                    question = json.loads(content)
                    #Remember to continue here
                elif statusCode == ResponseStatusCode.ANSWER_REQUIRED:
                    turnDetails = json.loads(content)
            
                    guessedCharacter = input("Please guess a character: ")

                    if turnDetails["keyword_guess_allowance"]:
                        guessedKeyword = input("Please guess the keyword (enter nothing if you do not want go guess): ")
                        if guessedKeyword == "": 
                            guessedKeyword = None
                    else:
                        guessedKeyword = None

                    self.sendRequest(Request(
                        statusCode = RequestStatusCode.ANSWER_SUBMISSION,
                        content = json.dumps({
                            "guessedCharacter": guessedCharacter,
                            "guessedKeyword": guessedKeyword
                        })
                    ))

    def run(self):
        
        listeningThread = threading.Thread(target = self.listen)
        
        listeningThread.start()            

        listeningThread.join()