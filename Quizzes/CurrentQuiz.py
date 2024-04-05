from Quiz import Quiz

class CurrentQuiz(Quiz):

    def __init__(self, quiz : Quiz) -> None:
        super().__init__(
            question = quiz.question, 
            keyword = quiz.keyword
        )
        self.hint = ["*" for _ in len(self.keyword)]

    def getHint(self) -> str:
        return "".join(self.hint)

    def receiveLetterGuess(self, letter : str) -> bool:

        letter = letter.strip().upper()

        if len(letter) != 1:
            return False

        result = False

        for i in range(len(self.keyword)):
            if self.keyword[i] == letter:
                self.hint[i] = letter
                result = True

        return result
    
    def receiveKeywordGuess(self, keyword : str) -> bool:
        
        if keyword.strip().upper() == self.keyword:
            self.hint = self.keyword
            return True
        
        return False