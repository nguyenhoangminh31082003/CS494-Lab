import pygame
import ColorCodeTuples

class Button:
	def __init__(self, buttonSize, buttonImage, containerInfo):
		self.size = (buttonSize[0], buttonSize[1])
		self.image = pygame.transform.scale(buttonImage, self.size)
		self.rect = self.image.get_rect()
		self.coord = (containerInfo[0] + (containerInfo[2] - self.size[0]) / 2, containerInfo[1] + (containerInfo[3] - self.size[1]) / 2)
		self.rect.topleft = self.coord
		self.clicked = False

	def draw(self, gameScreen):
		gameScreen.blit(self.image, (self.rect.x , self.rect.y))

	def fillColor(self, gameScreen):
		gameScreen.blit(self.image, (self.rect.x , self.rect.y))
		pygame.draw.rect(gameScreen, ColorCodeTuples.B_COLOR, pygame.Rect(self.coord[0], self.coord[1], self.size[0], self.size[1]))


	def isClicked(self): 
		action = False 

		pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(pos) :
			if(pygame.mouse.get_pressed()[0] == 1  and self.clicked == False):
				self.clicked = True
				action = True 
		if(pygame.mouse.get_pressed()[0] == 0): 
			self.clicked = False 
		return action 

	def resize(self, containerInfo, newSize, *args, **kwargs):
		self.size = (newSize[0], newSize[1])
		self.image = pygame.transform.scale(self.image, self.size)
		self.coord = (containerInfo[0] + (containerInfo[2] - self.size[0]) / 2, containerInfo[1] + (containerInfo[3] - self.size[1]) / 2)
		self.rect = self.image.get_rect()
		self.rect.topleft = self.coord
