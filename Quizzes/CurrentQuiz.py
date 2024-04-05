from Quiz import Quiz

class CurrentQuiz(Quiz):

    def __init__(self, quiz : Quiz) -> None:
        super().__init__(
            question = quiz.question, 
            keyword = quiz.keyword
        )
        
        self.currentKeyword = ["*" for _ in range(len(self.keyword))]

    def getCurrentKeyword(self) -> str:
        return "".join(self.currentKeyword)

    def receiveLetterGuess(self, letter : str) -> bool:

        letter = letter.strip().upper()

        if len(letter) != 1:
            return False

        result = False

        for i in range(len(self.keyword)):
            if self.keyword[i] == letter:
                self.currentKeyword[i] = letter
                result = True

        return result
    
    def receiveKeywordGuess(self, keyword : str) -> bool:
        
        if keyword.strip().upper() == self.keyword:
            self.currentKeyword = self.keyword
            return True
        
        return False
    
    def getKeywordLength(self) -> str:
        return len(self.keyword)