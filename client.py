from socket import * 
from enum import Enum
import json
import random
from rules import *

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((SERVER_NAME, SERVER_PORT))
unregister = True

def send(msg, type):
    message = process_message(msg, type)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client_socket.send(send_length)
    client_socket.send(message)

def receive():
    msg_length = client_socket.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        modified_sentence = client_socket.recv(msg_length).decode(FORMAT)
        modified_sentence = json.loads(modified_sentence)
        if modified_sentence.get("type") == SMessage.DISCONNECT.value:
            print("[SERVER DISCONNECT] Shutdown connection")
            client_socket.close()
            exit()
        if modified_sentence.get("type") == SMessage.ERROR.value:
            print("[SERVER ERROR]", modified_sentence['msg'])
            return False
        print("[SERVER MESSAGE]", modified_sentence['msg'])
    return True

def register():
    register = False
    while not register:
        name = input("Input your name: ")
        send(name, CMessage.REGISTER)
        register = receive()

register()
while connection_state:
    # client_socket.setblocking(False)
    option = input("(1: word, 2: keyword): ")
    sentence = input("Input your guess: ")
    if sentence == "exit":
        send("", CMessage.DISCONNECT)
    send(sentence, CMessage.WORD if option == "1" else CMessage.KEYWORD)
    connection_state = receive()