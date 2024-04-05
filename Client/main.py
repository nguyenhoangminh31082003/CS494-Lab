import sys

sys.path.append("./Server/")

from ClientModel import ClientModel
from ServerModel import ServerModel

if __name__ == "__main__":

    serverAddress = ServerModel.getStoredServerInformation()

    client = ClientModel()
    client.connectToServer(serverAddress["host"], serverAddress["port"])
    client.run()