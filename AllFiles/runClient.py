import sys
import threading

from ClientModel import ClientModel
from ServerModel import ServerModel
from GameGUI import GameGUI

if __name__ == "__main__":

    serverAddress = ServerModel.getStoredServerInformation()
    client = ClientModel()
    gameUI = GameGUI(client)
    
    client.connectToServer(serverAddress["host"], serverAddress["port"])

    backendThread = threading.Thread(target=client.listen)
    frontendThread = threading.Thread(target=gameUI.run)

    backendThread.start()
    frontendThread.start()

    frontendThread.join()
    backendThread.join()