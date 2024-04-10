import pygame
import json
import sys
import os

sys.path.append("Client/")

from ScreenViewID import ScreenViewID
from ClientModel import ClientModel
from TextBox import TextBox
import AssetConstants

class GameGUI:
    
    def __init__(self):
        self.screenViewID = ScreenViewID.REGISTER
        self.information = None
        self.running = False
        self.screen = None
        self.clock = None

        self.openScreenComponents = dict()
        self.waitScreenComponents = dict()
        self.gameScreenComponents = dict()
        self.loseScreenComponents = dict()
        self.statisticScreenComponents = dict()

    def initializeScreenComponents(self):
        containerBoxContainer = (
            GUI.screenWidth * 350 / 1000, GUI.screenHeight * 170 / 563, GUI.screenWidth * 332 / 1000, GUI.screenHeight * 332 / 563)

        self.open['label'] = TextBox.Text(
            AssetConstants.AMATICSC_FONT,
            AssetConstants.BLACK,
            32,
            AssetConstants.ENTER_NICKNAME,
            (containerBoxContainer[0], containerBoxContainer[1] + containerBoxContainer[3] / 2, containerBoxContainer[2], containerBoxContainer[3] * 15 / 100)
        )
        
        GUI.wait['hello'] = TextClass.Text(
            Constant.AMATICSC_FONT,
            Constant.BLACK,
            32,
            "Hello, ",
            (containerBoxContainer[0], containerBoxContainer[1] + containerBoxContainer[3] / 2 - GUI.screenHeight * 20 / 100, containerBoxContainer[2], containerBoxContainer[3] * 15 / 100)
        )
        
        GUI.wait['label'] = TextClass.Text(
            Constant.AMATICSC_FONT,
            Constant.BLACK,
            32,
            Constant.PAUSE_TEXT,
            (containerBoxContainer[0], containerBoxContainer[1] + containerBoxContainer[3] / 2, containerBoxContainer[2], containerBoxContainer[3] * 15 / 100)
        )
        
        GUI.open['notify'] = TextClass.Text(
            Constant.AMATICSC_FONT,
            Constant.WHITE,
            20,
            "",
            (containerBoxContainer[0], containerBoxContainer[1] + containerBoxContainer[3] / 2 + GUI.screenHeight * 6 / 100, containerBoxContainer[2], containerBoxContainer[3] * 15 / 100)
        )
        
        GUI.wait['notify'] = TextClass.Text(
            Constant.AMATICSC_FONT,
            Constant.GREEN,
            16,
            "1/5",
            (containerBoxContainer[0], containerBoxContainer[1] + containerBoxContainer[3] / 2 + GUI.screenHeight * 10 / 100, containerBoxContainer[2], containerBoxContainer[3] * 15 / 100)
        )
        
        # Nickname TextForm
        GUI.open['nickname'] = TextFormClass.TextForm(
            Constant.AMATICSC_FONT,
            Constant.BLACK,
            20,
            (containerBoxContainer[0], containerBoxContainer[1] + containerBoxContainer[3] / 2 + GUI.screenHeight * 13 / 100, containerBoxContainer[2], containerBoxContainer[3] * 15 / 100)
        )
        
        for i in range(26):
            text = f"{chr(65+i)}"
            x = containerBoxContainer[0] - GUI.screenWidth * 1 / 10 + ( i % 9 ) * 36
            y = containerBoxContainer[1] + GUI.screenHeight * 28 / 100 + (i // 9) * 36
            GUI.btns.append(ButtonClass.TextButton(text, x, y))
        
        for i in range(len(GUI.players_List)):
            player = list(GUI.players_List.keys())[i]
            score = list(GUI.players_List.values())[i]
            GUI.players.append((
                TextClass.Text(
                Constant.AMATICSC_FONT,
                Constant.WHITE,
                16,
                player,
                (GUI.screenWidth / 20, GUI.screenHeight / 10 + (i + 1) * 30, 0, 0),
            ),
              TextClass.Text(
                Constant.AMATICSC_FONT,
                Constant.WHITE,
                16,
                ": " + str(score),
                (GUI.screenWidth / 8, GUI.screenHeight / 10 + (i + 1) * 30, 0, 0),
            ))
                )
        
        GUI.game['round'] = TextClass.Text(
            Constant.AMATICSC_FONT,
            Constant.WHITE,
            30,
            "Round: 1",
            (containerBoxContainer[0], GUI.screenHeight / 10, containerBoxContainer[2], containerBoxContainer[3] * 15 / 100),
            True
        )
        
        GUI.game['player'] = TextClass.Text(
            Constant.AMATICSC_FONT,
            Constant.WHITE,
            20,
            "Players:",
            (GUI.screenWidth / 10, GUI.screenHeight / 10, 0, 0),
            True
        )
        
        GUI.game['Time'] = TextClass.Text(
            Constant.AMATICSC_FONT,
            Constant.WHITE,
            20,
            "Time",
            (GUI.screenWidth * 9 / 10, GUI.screenHeight / 10, 0, 0),
            True
        )
        
        GUI.game['Timer'] = TextClass.Text(
            Constant.AMATICSC_FONT,
            Constant.WHITE,
            20,
            str(GUI.timeLeft),
            (GUI.screenWidth * 9 / 10, GUI.screenHeight / 10 + 30, 0, 0),
        )

        # Start Button
        GUI.open['playButton'] = ButtonClass.Button(
            (GUI.screenWidth * 8 / 100, GUI.screenWidth * 8 / 100),
            Constant.PLAY_BUTTON,
            (containerBoxContainer[0], containerBoxContainer[1] + containerBoxContainer[3] / 2 + GUI.screenHeight * 25 / 100, containerBoxContainer[2], GUI.screenHeight - (containerBoxContainer[1] + containerBoxContainer[3]))
        )

    def initialize(self):
        pygame.init()
        
        self.information = self.getGUIInformation()
        
        pygame.display.set_caption(self.information["title"])

        self.screen = pygame.display.set_mode(
            (
                self.information["screen_size"]["width"], 
                self.information["screen_size"]["height"]
            ),
            pygame.RESIZABLE
        )

        self.clock = pygame.time.Clock()
        self.running = True

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

    def displayRegisterScreen(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pass

    def run(self):
        self.initialize()

        pygame.time.set_timer(pygame.USEREVENT, 1000)

        while self.running:
            self.clock.tick(self.information["frame_rate"])

            if self.screenViewID == ScreenViewID.REGISTER:  
                self.displayRegisterScreen()

            if not self.running:
                break

            pygame.display.update()