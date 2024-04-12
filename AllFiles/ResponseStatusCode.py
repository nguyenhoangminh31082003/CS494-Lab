import enum

class ResponseStatusCode(enum.IntEnum):
    NICKNAME_REQUIREMENT = 1
    INVALID_NICKNAME = 2
    NICKNAME_ALREADY_TAKEN = 3
    NICKNAME_ACCEPTED = 4
    BROADCASTED_MESSAGE = 5
    GAME_FULL = 6
    ANSWER_REQUIRED = 8
    QUESTION_SENT = 9
    GAME_ENDED = 10
    BROADCASTED_SUMMARY = 11
    GAME_STARTED = 12
    BROADCASTED_PLAYER_ANSWER = 13
    BROADCASTED_RANK = 14
    RESTART_ALLOWED = 15
    WAIT_GAME_START_REQUIRED = 16
    SERVER_CLOSE_CONNECTION = 17

    def isNicknameRelated(self) -> bool:
        return self in [
            ResponseStatusCode.NICKNAME_REQUIREMENT, 
            ResponseStatusCode.INVALID_NICKNAME, 
            ResponseStatusCode.NICKNAME_ALREADY_TAKEN, 
            ResponseStatusCode.NICKNAME_ACCEPTED
        ]