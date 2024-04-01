import sys
sys.path.append("../")

import Client.ClientModel as ClientModel

if __name__ == "__main__":
    client = ClientModel.Client({"host": "127.0.0.1", "port": 12000})
    client.run()