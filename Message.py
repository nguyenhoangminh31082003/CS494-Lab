import json

class Message:

    def __init__(self):
        self.data = dict()

    def deserialize(self, data) -> None:
        self.data = json.loads(data)

    def getStatusCode(self):
        return self.data["status_code"]

    def getContent(self):
        return self.data["content"]
    
    def toString(self):
        return json.dumps(self.data)
    