import json

from Message import Message
from ResponseStatusCode import ResponseStatusCode

class Response(Message):

    def __init__(self, statusCode : ResponseStatusCode, content : str):
        super().__init__()
        self.data["status_code"] = statusCode
        self.data["content"] = content

    @staticmethod
    def getDeserializedResponse(data : str):
        dictionary = json.loads(data)
        response = Response(
            statusCode = ResponseStatusCode(dictionary["status_code"]), 
            content = dictionary["content"]
        )
        return response

    