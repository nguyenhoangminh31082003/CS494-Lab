import sys
import json
import threading

sys.path.append("./Server/")
sys.path.append("./GUI/")
sys.path.append("./Message/")
sys.path.append("./Message/")

import Constant 
from MenuClass import GUI
from Request import Request
from Response import Response
from ClientModel import ClientModel
from ServerModel import ServerModel
from RequestStatusCode import RequestStatusCode
from ResponseStatusCode import ResponseStatusCode


if __name__ == "__main__":

    serverAddress = ServerModel.getStoredServerInformation()
    client = ClientModel()
    client.connectToServer(serverAddress["host"], serverAddress["port"])

    backendThread = threading.Thread(target=client.listen)
    backendThread.start()
    backendThread.join()

    if False:
        gui = GUI()
        
        def handleRegistration(statusCode: ResponseStatusCode, content: str) -> None:
            if statusCode == ResponseStatusCode.NICKNAME_ACCEPTED:
                print(content)
                return

            client.nickname = None
                    
            if statusCode == ResponseStatusCode.NICKNAME_REQUIREMENT:
                client.nickname = input("Please enter your nickname: ")
            elif statusCode == ResponseStatusCode.INVALID_NICKNAME:
                client.nickname = input("The chosen nickname is not valid. Please enter a valid nickname: ")
            elif statusCode == ResponseStatusCode.NICKNAME_ALREADY_TAKEN:
                client.nickname = input("The chosen nickname is already taken. Please enter another nickname: ")
                    
            if client.nickname is not None:
                client.sendRequest(Request(
                    statusCode = RequestStatusCode.NICKNAME_REQUEST, 
                    content = client.nickname
                ))

        def handleAnswerSubmission(turnDetails: dict) -> None:
                
            guessedCharacter = input("Please guess a character: ")
            guessedKeyword = None

            if turnDetails["keyword_guess_allowance"]:
                guessedKeyword = input("Please guess the keyword (enter nothing if you do not want go guess): ")
                if guessedKeyword == "": 
                    guessedKeyword = None

            client.sendRequest(Request(
            statusCode = RequestStatusCode.ANSWER_SUBMISSION,
                content = json.dumps({
                    "guessed_character": guessedCharacter,
                    "guessed_keyword": guessedKeyword
                })
            ))

        def closeConnection():
            client.clientSocket.close()

        def listen():
            while True:
                receivedData = client.clientSocket.recv(1024).decode()
                
                if receivedData:
                    response = Response.getDeserializedResponse(receivedData)

                    statusCode = response.getStatusCode()
                    content = response.getContent()

                    if statusCode.isNicknameRelated():
                        handleRegistration(statusCode, content)        
                    elif statusCode == ResponseStatusCode.BROADCASTED_MESSAGE:
                        print(content)
                    elif statusCode == ResponseStatusCode.BROADCASTED_SUMMARY:
                        client.summary = json.loads(content)
                        #print(json.dumps(client.summary, indent = 4))
                    elif statusCode == ResponseStatusCode.GAME_FULL:
                        print(content)
                        #This block might be changed in the future
                    elif statusCode == ResponseStatusCode.GAME_ENDED:
                        print(content)
                        closeConnection()
                        break
                    elif statusCode == ResponseStatusCode.QUESTION_SENT:
                        question = json.loads(content)
                    elif statusCode == ResponseStatusCode.ANSWER_REQUIRED:
                        handleAnswerSubmission(json.loads(content))
        
        guiThread = threading.Thread(target=gui.run)
        listeningThread = threading.Thread(target=listen)
        guiThread.start()
        listeningThread.start()
        
        listeningThread.join()
        guiThread.join()    