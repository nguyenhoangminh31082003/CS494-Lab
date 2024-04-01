import threading
import socket

import sys
sys.path.append("../")

class Client:
    def __init__(self, address: dict):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((address["host"], int(address["port"])))
        
    def handleAnIteration(self):
        message = self.client.recv(1024).decode()
        if message == "Please enter your nickname: ":
            nickname = input(message)
            self.client.send(nickname.encode())
            return

    def run(self):
        thread = threading.Thread(target=self.handleAnIteration)
        thread.start()
