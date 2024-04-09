

class GUIModel:
    order = 1
    turnOfPlayer = 3
    gameTurn = 2
    total = 5
    nickname = ''
    point = 0
    fullWord = ''
    hint = 'One of the most popular interpreter programming languages.'
    guessLetter = ''

    def __init__(self, nickname, point, fullWord, guessLetter):
        GUIModel.nickname = nickname
        GUIModel.point = point
        GUIModel.fullWord = fullWord
        GUIModel.guessLetter = guessLetter