from typing import Any
import pygame

from TextBox import TextBox

class TextForm(TextBox):
    def __init__(self, textFont, textColor, textSize, containerInfo, maxChar = 10):
        super().__init__(textFont, textColor, textSize, "", containerInfo)
        self.isSelected = False
        self.inputRect = pygame.Rect(containerInfo[0], containerInfo[1], containerInfo[2], containerInfo[3])
        self.maxChar = maxChar
    def select(self):
        self.isSelected = True
        
    def deselect(self):
        self.isSelected = False
        
    def getText(self):
        return self.textContent
    
    def addText(self, unicode):
        # check if unicode is backspace
        if unicode == "\x08":
            self.changeTextContent(self.textContent[:-1])
        elif len(self.textContent) >= self.maxChar or ( not unicode.isalnum() and not unicode in [" ", ".", ",", "!", "?"]):
            return
        else:
            self.changeTextContent(self.textContent + unicode)
	
    def draw(self, gameScreen):
        # draw the inputRect
        pygame.draw.rect(gameScreen, (255, 255, 255), self.inputRect)
        gameScreen.blit(self.text, (self.inputRect.x + 10, self.inputRect.y))
    
    def resize(self, containerInfo, *args, **kwargs):
        super().resize(containerInfo, *args, **kwargs)
        self.inputRect = pygame.Rect(containerInfo[0], containerInfo[1], containerInfo[2], containerInfo[3])
        