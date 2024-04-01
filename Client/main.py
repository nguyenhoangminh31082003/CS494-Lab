import sys
sys.path.append("../")
sys.path.append("./Server/")

import Client
import Server

if __name__ == "__main__":
    client = Client.Client(Server.Server.getAddress())

    client.run()