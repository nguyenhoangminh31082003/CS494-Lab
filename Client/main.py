import sys
import json
import threading

sys.path.append("./GUI/")
sys.path.append("./Server/")
sys.path.append("./Message/")

import Constant 
from GameGUI import GameGUI
from Request import Request
from Response import Response
from ClientModel import ClientModel
from ServerModel import ServerModel
from RequestStatusCode import RequestStatusCode
from ResponseStatusCode import ResponseStatusCode


if __name__ == "__main__":

    serverAddress = ServerModel.getStoredServerInformation()
    client = ClientModel()
    gui = GameGUI(client)
    
    client.connectToServer(serverAddress["host"], serverAddress["port"])

    backendThread = threading.Thread(target=client.listen)
    guiThread = threading.Thread(target=gui.run)

    backendThread.start()
    guiThread.start()

    guiThread.join()
    backendThread.join()