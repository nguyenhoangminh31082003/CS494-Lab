import MenuClass
import pygame

# Init
pygame.init()
infoObject = pygame.display.Info()
screenProportion = 1/2

menuGame = MenuClass.GUI()
menuGame.run()