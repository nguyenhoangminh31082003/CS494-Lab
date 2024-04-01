from socket import * 
from threading import Thread, active_count
import json
from rules import *
import random

client_list = []
client_name = {}
turn = 0
DEMO = 'DEMO'

server_socker = socket(AF_INET, SOCK_STREAM)
server_socker.bind((SERVER_NAME, SERVER_PORT))

word_list = {}
# read data from data.txt to get the list of words
with open("data.txt", "r") as file:
    number_of_words = int(file.readline())
    # read all the words
    # for each line has format <word>: <hint>
    for _ in range(number_of_words):
        word, hint = file.readline().split(":")
        word_list[word.strip().upper()] = hint.strip()
    WORD = random.choice(list(word_list.keys()))
    HINT = word_list[WORD]
    encoded_word = "*" * len(WORD)



def guess_keyword(keyword: str):
    if keyword.strip().upper() in WORD:
        return True
    return False

def guess_word(word: str):
    if word.strip().upper() in WORD:
        return True
    return False

def handle_client(connection_socket, addr):
    def quiz():
        msg = f"Guess the word: {encoded_word}\nNumber of words: {len(WORD)}\nHint: {HINT}"
        send(msg, SMessage.MESSAGE)
        print(f"[{addr}]: Sent quiz message")
        
    def send(msg: str, type = SMessage.MESSAGE):
        message = process_message(msg, type)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        connection_socket.send(send_length)
        connection_socket.send(message)
        
    def receive(function: callable):
        msg_length = connection_socket.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            raw = connection_socket.recv(msg_length).decode(FORMAT)
            sentence = json.loads(raw)
            print(f"[{addr} RECEIVED]: ", sentence['msg'])
            if sentence.get("type") == CMessage.DISCONNECT.value:
                print("Server is down")
                return False
            function(sentence['msg'])
        return True
    
    def handle_register(msg):
        global client_name, client_list
        unresiter = False
        if msg in client_name:
            send(f"Name {msg} is already taken, please choose another one", SMessage.FAIL)
            print("Register Failed")
            register = True
        else:
            send(f"Register {msg} successfully", SMessage.SUCCESS)
            client_name[msg] = addr
            client_list.append(addr)
            print("Register Successfully")
            register = False
        return register
        
    def handle_message(msg):
        global turn, client_list
        if len(client_list) == 1:
            send("Wait for another player to join", SMessage.MESSAGE)
            return
        if client_list.index(addr) != turn:
            send("It's not your turn", SMessage.FAIL)
            return
        processed_msg = msg.upper()
        turn = (turn + 1) % len(client_list)
        send(processed_msg)
        print(f"[{addr}]: {msg} -> {processed_msg}")
    
    print(f"[NEW CONNECTION] {addr} connected.")
    while True:
        t = receive(lambda msg: handle_register(msg))
        if not t:
            break
        print(t)
    print(f"[{addr}]: mibang")
    connected = True
    try:
        while connected == True:
            quiz()
            connected = receive(lambda msg: handle_message(msg))
    except:
        pass
    finally:
        print(f"[{addr}]: disconnected")
        send({"type": CMessage.DISCONNECT.value, "msg": "Server is down"})
        connection_socket.close()  # Close the socket to ensure the thread stops
        client_list.remove(addr)

def start():
    server_socker.listen()
    print(f"[LISTENING] Server is listening on {SERVER_NAME}:{SERVER_PORT}")
    while True:
        connection_socket, addr = server_socker.accept()
        thread = Thread(target=handle_client, args=(connection_socket, addr))
        thread.start()
        print("[ACTIVE CONNECTIONS]", active_count() - 1)
        


print("[STARTING] server is starting...")        
start()