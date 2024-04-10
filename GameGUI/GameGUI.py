import pygame
import json
import sys
import os

sys.path.append("Client/")

from ScreenViewID import ScreenViewID
from ClientModel import ClientModel
from TextForm import TextForm
from TextBox import TextBox
import MessageTextConstants
from Button import Button
import ColorCodeTuples
import AssetConstants

class GameGUI:
    
    def __init__(self):
        self.screenViewID = ScreenViewID.REGISTER
        self.information = None
        self.running = False
        self.screen = None
        self.clock = None

        self.screenWidth = None
        self.screenHeight = None

        self.openScreenComponents = dict()
        self.waitScreenComponents = dict()
        self.gameScreenComponents = dict()
        self.loseScreenComponents = dict()
        self.statisticScreenComponents = dict()

    def initializeScreenComponents(self):
        containerBoxContainer = (
            self.screenWidth * 350 / 1000, 
            self.screenHeight * 170 / 563, 
            self.screenWidth * 332 / 1000, 
            self.screenHeight * 332 / 563
        )

        self.open['label'] = TextBox(
            AssetConstants.AMATICSC_FONT,
            ColorCodeTuples.BLACK,
            32,
            MessageTextConstants.ENTER_NICKNAME,
            (containerBoxContainer[0], containerBoxContainer[1] + containerBoxContainer[3] / 2, containerBoxContainer[2], containerBoxContainer[3] * 15 / 100)
        )
        
        self.wait['hello'] = TextBox(
            AssetConstants.AMATICSC_FONT,
            ColorCodeTuples.BLACK,
            32,
            "Hello, ",
            (containerBoxContainer[0], containerBoxContainer[1] + containerBoxContainer[3] / 2 - self.screenHeight * 20 / 100, containerBoxContainer[2], containerBoxContainer[3] * 15 / 100)
        )
        
        self.wait['label'] = TextBox(
            AssetConstants.AMATICSC_FONT,
            ColorCodeTuples.BLACK,
            32,
            MessageTextConstants.PAUSE_TEXT,
            (containerBoxContainer[0], containerBoxContainer[1] + containerBoxContainer[3] / 2, containerBoxContainer[2], containerBoxContainer[3] * 15 / 100)
        )
        
        self.open['notify'] = TextBox(
            AssetConstants.AMATICSC_FONT,
            ColorCodeTuples.WHITE,
            20,
            "",
            (containerBoxContainer[0], containerBoxContainer[1] + containerBoxContainer[3] / 2 + self.screenHeight * 6 / 100, containerBoxContainer[2], containerBoxContainer[3] * 15 / 100)
        )
        
        self.wait['notify'] = TextBox(
            AssetConstants.AMATICSC_FONT,
            ColorCodeTuples.GREEN,
            16,
            "1/5",
            (containerBoxContainer[0], containerBoxContainer[1] + containerBoxContainer[3] / 2 + self.screenHeight * 10 / 100, containerBoxContainer[2], containerBoxContainer[3] * 15 / 100)
        )
        
        # Nickname TextForm
        self.open['nickname'] = TextForm(
            AssetConstants.AMATICSC_FONT,
            ColorCodeTuples.BLACK,
            20,
            (containerBoxContainer[0], containerBoxContainer[1] + containerBoxContainer[3] / 2 + self.screenHeight * 13 / 100, containerBoxContainer[2], containerBoxContainer[3] * 15 / 100)
        )
        
        for i in range(26):
            text = f"{chr(65+i)}"
            x = containerBoxContainer[0] - self.screenWidth * 1 / 10 + ( i % 9 ) * 36
            y = containerBoxContainer[1] + self.screenHeight * 28 / 100 + (i // 9) * 36
            self.btns.append(Button.TextButton(text, x, y))
        
        for i in range(len(self.players_List)):
            player = list(self.players_List.keys())[i]
            score = list(self.players_List.values())[i]
            self.players.append((
                TextBox.Text(
                AssetConstants.AMATICSC_FONT,
                ColorCodeTuples.WHITE,
                16,
                player,
                (self.screenWidth / 20, self.screenHeight / 10 + (i + 1) * 30, 0, 0),
            ),
              TextBox.Text(
                AssetConstants.AMATICSC_FONT,
                ColorCodeTuples.WHITE,
                16,
                ": " + str(score),
                (self.screenWidth / 8, self.screenHeight / 10 + (i + 1) * 30, 0, 0),
            ))
                )
        
        self.game['round'] = TextBox.Text(
            AssetConstants.AMATICSC_FONT,
            ColorCodeTuples.WHITE,
            30,
            "Round: 1",
            (containerBoxContainer[0], self.screenHeight / 10, containerBoxContainer[2], containerBoxContainer[3] * 15 / 100),
            True
        )
        
        self.game['player'] = TextBox.Text(
            AssetConstants.AMATICSC_FONT,
            ColorCodeTuples.WHITE,
            20,
            "Players:",
            (self.screenWidth / 10, self.screenHeight / 10, 0, 0),
            True
        )
        
        self.game['Time'] = TextBox.Text(
            AssetConstants.AMATICSC_FONT,
            ColorCodeTuples.WHITE,
            20,
            "Time",
            (self.screenWidth * 9 / 10, self.screenHeight / 10, 0, 0),
            True
        )
        
        self.game['Timer'] = TextBox.Text(
            AssetConstants.AMATICSC_FONT,
            ColorCodeTuples.WHITE,
            20,
            str(self.timeLeft),
            (self.screenWidth * 9 / 10, self.screenHeight / 10 + 30, 0, 0),
        )

        self.open['playButton'] = Button(
            (self.screenWidth * 8 / 100, self.screenWidth * 8 / 100),
            MessageTextConstants.PLAY_BUTTON,
            (containerBoxContainer[0], containerBoxContainer[1] + containerBoxContainer[3] / 2 + self.screenHeight * 25 / 100, containerBoxContainer[2], self.screenHeight - (containerBoxContainer[1] + containerBoxContainer[3]))
        )

    def initializeImages(self):
        self.backgroundImage = pygame.transform.scale(
            AssetConstants.MENU, 
            (
                self.screenWidth, 
                self.screenHeight
            )
        )

        self.inGameImage = pygame.transform.scale(
            AssetConstants.BACKGROUND, 
            (
                self.screenWidth, 
                self.screenHeight
            )
        )

    def initialize(self):
        pygame.init()
        
        self.information = self.getGUIInformation()
        
        pygame.display.set_caption(self.information["title"])

        self.screenWidth = self.information["screen_size"]["width"]
        self.screenHeight = self.information["screen_size"]["height"]

        self.screen = pygame.display.set_mode(
            (
                self.screenWidth,
                self.screenHeight
            ),
            pygame.RESIZABLE
        )

        self.clock = pygame.time.Clock()
        self.running = True

        self.initializeImages()

        self.initializeScreenComponents()

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

    def resize(self):
        self.screenWidth, self.screenHeight = pygame.display.get_surface().get_size()
        self.backgroundImage = pygame.transform.scale(
            AssetConstants.MENU, 
            (
                self.screenWidth, 
                self.screenHeight
            )
        )

        containerBoxContainer = (self.screenWidth * 350 / 1000, self.screenHeight * 170 / 563, self.screenWidth * 332 / 1000, self.screenHeight * 332 / 563)
        elementSize = (self.screenWidth * 8 / 100, self.screenWidth * 8 / 100)
        for element in self.open.values():
            element.resize(containerBoxContainer, elementSize)

    def validateNickname(self):
        if self.open['nickname'].getText() == "":
            self.open['notify'].changeTextContent(MessageTextConstants.INVALID_MESSAGE_REGISTER)
            return False
        return True

    def displayRegisterScreen(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:
                    if self.validateNickname():
                        self.nickname = self.openScreenComponents['nickname'].getText()
                        self.waitScreenComponents['hello'].changeTextContent("Hello, " + self.nickname + "!")
                        self.screenViewID = ScreenViewID.WAIT
                        return
                self.openScreenComponents['notify'].changeTextContent("")
                self.openScreenComponents['nickname'].addText(event.unicode)
          
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_presses = pygame.mouse.get_pressed()
            elif pygame.VIDEORESIZE:
                pass

    @staticmethod
    def registerScreen():
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    GUI.running = False
                    pygame.quit()
                    exit(0)
                case pygame.KEYDOWN:
                    # if the key is enter, validate the nickname
                    if event.key == pygame.K_RETURN:
                        if GUI.validateNickname():
                            GUI.nickname = GUI.open['nickname'].getText()
                            GUI.wait['hello'].changeTextContent("Hello, " + GUI.nickname + "!")
                            GUI.ScreenView = Constant.ScreenView.WAIT
                            return
                    GUI.open['notify'].changeTextContent("")
                    GUI.open['nickname'].addText(event.unicode)
                case pygame.MOUSEBUTTONDOWN:
                    mouse_presses = pygame.mouse.get_pressed()
                # when the screen is resized, scale the open
                case pygame.VIDEORESIZE:
                    # GUI.resize()
                    pass

        # Start Button Process
        startButtonState = GUI.open['playButton'].isClicked()

        if startButtonState == True:
            if GUI.validateNickname():
                GUI.nickname = GUI.open['nickname'].getText()
                GUI.wait['hello'].changeTextContent("Hello, " + GUI.nickname + "!")
                GUI.ScreenView = Constant.ScreenView.WAIT
        # Draw Window
        GUI.gameScreen.blit(GUI.backgroundImage, (0, 0))
        for element in GUI.open.values():
            element.draw(GUI.gameScreen)
        pygame.display.update()
    
    @staticmethod
    def waitScreen():
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    GUI.running = False
                    pygame.quit()
                    exit(0)
                case pygame.MOUSEBUTTONDOWN:
                    GUI.ScreenView = Constant.ScreenView.GAME
        GUI.gameScreen.blit(GUI.inGameImage, (0, 0))
        for element in GUI.wait.values():
            element.draw(GUI.gameScreen)
        pygame.display.update()
        
    
    @staticmethod
    def matchScreen():
        pos = None
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    GUI.running = False
                    pygame.quit()
                    exit(0)
                case pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                case pygame.USEREVENT:
                    if GUI.timeLeft and not GUI.submit:
                        GUI.timeLeft -= 1
                        GUI.game['Timer'].changeTextContent(str(GUI.timeLeft))
        GUI.gameScreen.blit(GUI.inGameImage, (0, 0))
        for element in GUI.game.values():
            element.draw(GUI.gameScreen)
        for btn in GUI.btns:
            btn.draw(GUI.gameScreen)
            if pos:
                if btn.collision(pos):
                    GUI.submit = True
        if GUI.timeLeft == 0:
            GUI.submit = True
        for i in range(len(GUI.word)):
            x = GUI.screenWidth // 2 - ((18 * len(GUI.word)) // 2)
            x1, y1 = (x + 20 * i,GUI.screenHeight // 2)
            x2, y2 = (x + 20 * i + 15, GUI.screenHeight // 2)
            pygame.draw.line(GUI.gameScreen, Constant.WHITE, (x1, y1), (x2, y2), 2)
        for i in range(len(GUI.players_List)):
            GUI.players[i][0].drawLeftToRight(GUI.gameScreen)
            GUI.players[i][1].drawLeftToRight(GUI.gameScreen)
            if i == GUI.turn: 
                GUI.players[i][0].changeColor(Constant.GREEN)
                GUI.players[i][1].changeColor(Constant.GREEN)
        pygame.display.update()
    
    @staticmethod
    def loseScreen():
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    GUI.running = False
                    pygame.quit()
                    exit(0)
        GUI.gameScreen.blit(GUI.inGameImage, (0, 0))
        for element in GUI.lose.values():
            element.draw(GUI.gameScreen)
        pygame.display.update()
    
    @staticmethod
    def statScreen():
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    GUI.running = False
                    pygame.quit()
                    exit(0)
        GUI.gameScreen.blit(GUI.inGameImage, (0, 0))
        for element in GUI.stat.values():
            element.draw(GUI.gameScreen)
        pygame.display.update()

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