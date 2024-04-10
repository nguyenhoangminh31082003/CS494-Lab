import pygame
import json
import sys
import os

sys.path.append("Client/")

from ClientModel import ClientModel

class GameGUI:
    
    def __init__(self):
        self.information = None
        self.screen = None

    def initialize(self):
        pygame.init()
        
        self.information = self.getGUIInformation()
        
        self.screen = pygame.display.set_mode(
            (
                self.information["screen_size"]["width"], 
                self.information["screen_size"]["height"]
            ),
            pygame.RESIZABLE
        )

    @staticmethod
    def getGUIInformation() -> dict:
        fileName = "./Data/GUI_information.json"

        if not os.path.exists(fileName):
            return {
                "screen_size": {
                    "width": 1300,
                    "height": 600
                }
            }
        
        with open(fileName, "r") as file:
            return json.load(file)

    def run(self):
        self.initialize()

        continued = True

        i = 0

        while continued:
            print("Running GUI")

            i  = (i + 1) % 255

            self.screen.fill((i, i, i))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    continued = False
                    print("GUI closed")
                    break

            if not continued:
                break

            pygame.display.update()