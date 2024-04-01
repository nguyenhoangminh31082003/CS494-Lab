from socket import socket, AF_INET, SOCK_STREAM
from enum import Enum
import json

SERVER_NAME = "localhost"
SERVER_PORT = 12000
HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "EXIT"

connection_state = True

CMessage = Enum("MessageType", ["REGISTER", "DISCONNECT", "KEYWORD", "WORD"])
SMessage = Enum("MessageType", ["SUCCESS", "MESSAGE", "SUMMARY", "DISCONNECT", "ERROR", "FAIL"])

def process_message(msg: str, type = SMessage.MESSAGE):
    json_msg =  {
        "msg": msg,
        "type": type.value
    }
    msg = json.dumps(json_msg)
    message = msg.encode(FORMAT)
    return message

