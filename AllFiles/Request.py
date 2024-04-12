import json

from Message import Message
from RequestStatusCode import RequestStatusCode

class Request(Message):

    def __init__(self, statusCode : RequestStatusCode, content : str):
        super().__init__()
        self.data["status_code"] = statusCode
        self.data["content"] = content

    @staticmethod
    def getDeserializedRequest(data : str):
        dictionary = json.loads(data)
        request = Request(
            statusCode = RequestStatusCode(dictionary["status_code"]), 
            content = dictionary["content"]
        )
        return request