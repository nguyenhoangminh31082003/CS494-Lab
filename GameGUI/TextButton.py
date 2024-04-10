import pygame

import AssetConstants
import ColorCodeTuples

class TextButton(pygame.sprite.Sprite):
	def __init__(self, text, x, y, textSize = 20):
		self.textFont = pygame.font.Font(AssetConstants.AMATICSC_FONT, textSize)
		self.text = text
		self.image = self.textFont.render(self.text, True, ColorCodeTuples.WHITE)
		self.rect = pygame.Rect(x, y, 30, 30)
		self.clicked = False
		
	def collision(self, pos):
		if pos and not self.clicked:
			if self.rect.collidepoint(pos):
				self.image = self.textFont.render(self.text, True, ColorCodeTuples.GREEN)
				self.clicked = True
				return True, self.text
		return False
		
	def draw(self, gameScreen):
		pygame.draw.rect(gameScreen, ColorCodeTuples.WHITE, self.rect, 2)
		gameScreen.blit(self.image, (self.rect.centerx - self.image.get_width() // 2, self.rect.centery - self.image.get_height() // 2))
		
	def reset(self):
		self.clicked = False
		self.image = self.textFont.render(self.text, True, ColorCodeTuples.WHITE)
		