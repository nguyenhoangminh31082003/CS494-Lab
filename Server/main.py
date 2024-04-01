import sys
sys.path.append("../")


import Server

if __name__ == "__main__":
    server = Server.Server()
    server.receiveClientRequestForConnection()