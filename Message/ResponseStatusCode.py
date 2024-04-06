import enum

class ResponseStatusCode(enum.IntEnum):
    NICKNAME_REQUIREMENT = 1
    INVALID_NICKNAME = 2
    NICKNAME_ALREADY_TAKEN = 3
    NICKNAME_ACCEPTED = 4
    BROADCASTED_MESSAGE = 5
    GAME_FULL = 6
    ANSWER_REQUIRED = 8