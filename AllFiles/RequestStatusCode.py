import enum

class RequestStatusCode(enum.IntEnum):
    NICKNAME_REQUEST = 1
    ANSWER_SUBMISSION = 2
    CLOSE_CONNECTION = 3
    RESTART_NEW_MATCH = 4