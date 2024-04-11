import pygame
import time
import json
import sys
import os

sys.path.append("./Client/")
sys.path.append("./Message/")

from ResponseStatusCode import ResponseStatusCode
from ScreenViewID import ScreenViewID
from ClientModel import ClientModel
from TextButton import TextButton
from Response import Response
from TextForm import TextForm
from TextBox import TextBox
import MessageTextConstants
from Button import Button
import ColorCodeTuples
import AssetConstants

class GameGUI:
    
    def __init__(self, client: ClientModel):
        self.screenViewID = ScreenViewID.REGISTER
        self.information = None
        self.running = False
        self.screen = None
        self.submit = False
        self.myTurn = False
        self.clock = None
        self.font = None
        

        self.screenWidth = None
        self.screenHeight = None

        self.openScreenComponents = dict()
        self.waitScreenComponents = dict()
        self.gameScreenComponents = dict()
        self.loseScreenComponents = dict()
        self.statisticScreenComponents = dict()

        self.buttons = []

        self.client = client
        self.scoreboard = []

        self.summary = None

        self.timeLeft = 20
        self.ranks = None

    def bindSummaryUI(self) -> bool:

        if self.summary is None:
            return False

        self.scoreboard.clear()

        playerInformation = self.summary["player"]["player_information"]
        currentPlayerNickname = self.summary["player"]["current_player"]

        for i, player in enumerate(playerInformation):
            
            if player["nickname"] is None:
                continue

            color = (ColorCodeTuples.GREEN if player["nickname"] == currentPlayerNickname else ColorCodeTuples.WHITE)
            
            self.scoreboard.append(
                (
                    TextBox(
                        textFont = AssetConstants.AMATICSC_FONT,
                        textColor = color,
                        textSize = 16,
                        textContent = player["nickname"],
                        containerInfo = (
                            self.screenWidth / 20, 
                            self.screenHeight / 10 + (i + 1) * 30, 0, 0
                        )
                    ),
                    TextBox(
                        textFont = AssetConstants.AMATICSC_FONT,
                        textColor = color,
                        textSize = 16,
                        textContent = f": {player['points']}",
                        containerInfo = (
                            self.screenWidth / 8, 
                            self.screenHeight / 10 + (i + 1) * 30, 0, 0
                        ),
                    )
                )
            )

        self.timeLeft = 20 - int(time.time() - self.summary["start_time"])
        self.gameScreenComponents['Timer'].changeTextContent(str(self.timeLeft))
        
        return True

    def initializeScreenComponents(self):
        containerBoxContainer = (
            self.screenWidth * 350 / 1000, 
            self.screenHeight * 170 / 563, 
            self.screenWidth * 332 / 1000, 
            self.screenHeight * 332 / 563
        )
        
        self.font = pygame.font.Font(AssetConstants.AMATICSC_FONT, 20)

        self.openScreenComponents['label'] = TextBox(
            AssetConstants.AMATICSC_FONT,
            ColorCodeTuples.BLACK,
            32,
            MessageTextConstants.ENTER_NICKNAME,
            (containerBoxContainer[0], containerBoxContainer[1] + containerBoxContainer[3] / 2, containerBoxContainer[2], containerBoxContainer[3] * 15 / 100)
        )
        
        self.waitScreenComponents['hello'] = TextBox(
            AssetConstants.AMATICSC_FONT,
            ColorCodeTuples.BLACK,
            32,
            "Hello, ",
            (containerBoxContainer[0], containerBoxContainer[1] + containerBoxContainer[3] / 2 - self.screenHeight * 20 / 100, containerBoxContainer[2], containerBoxContainer[3] * 15 / 100)
        )
        
        self.waitScreenComponents['label'] = TextBox(
            AssetConstants.AMATICSC_FONT,
            ColorCodeTuples.BLACK,
            32,
            MessageTextConstants.PAUSE_TEXT,
            (containerBoxContainer[0], containerBoxContainer[1] + containerBoxContainer[3] / 2, containerBoxContainer[2], containerBoxContainer[3] * 15 / 100)
        )
        
        self.openScreenComponents['notify'] = TextBox(
            AssetConstants.AMATICSC_FONT,
            ColorCodeTuples.WHITE,
            20,
            "",
            (containerBoxContainer[0], containerBoxContainer[1] + containerBoxContainer[3] / 2 + self.screenHeight * 6 / 100, containerBoxContainer[2], containerBoxContainer[3] * 15 / 100)
        )
        
        self.waitScreenComponents['notify'] = TextBox(
            AssetConstants.AMATICSC_FONT,
            ColorCodeTuples.GREEN,
            16,
            "1/5",
            (containerBoxContainer[0], containerBoxContainer[1] + containerBoxContainer[3] / 2 + self.screenHeight * 10 / 100, containerBoxContainer[2], containerBoxContainer[3] * 15 / 100)
        )
        
        # Nickname TextForm
        self.openScreenComponents['nickname'] = TextForm(
            AssetConstants.AMATICSC_FONT,
            ColorCodeTuples.BLACK,
            20,
            (containerBoxContainer[0], containerBoxContainer[1] + containerBoxContainer[3] / 2 + self.screenHeight * 13 / 100, containerBoxContainer[2], containerBoxContainer[3] * 15 / 100)
        )
        
        for i in range(26):
            text = f"{chr(65+i)}"
            x = containerBoxContainer[0] - self.screenWidth * 1 / 10 + ( i % 9 ) * 36
            y = containerBoxContainer[1] + self.screenHeight * 28 / 100 + (i // 9) * 36
            self.buttons.append(TextButton(text, x, y))
        
        self.gameScreenComponents['round'] = TextBox(
            AssetConstants.AMATICSC_FONT,
            ColorCodeTuples.WHITE,
            30,
            "abcxyzk - Round: 1",
            (containerBoxContainer[0], self.screenHeight / 10, containerBoxContainer[2], containerBoxContainer[3] * 15 / 100),
            True
        )
        
        self.gameScreenComponents['hint'] = TextBox(
            AssetConstants.AMATICSC_FONT,
            ColorCodeTuples.WHITE,
            16,
            "hint",
            (containerBoxContainer[0], self.screenHeight * 2 / 10, containerBoxContainer[2], containerBoxContainer[3] * 15 / 100),
        )
        
        self.gameScreenComponents['player'] = TextBox(
            AssetConstants.AMATICSC_FONT,
            ColorCodeTuples.WHITE,
            20,
            "Players:",
            (self.screenWidth / 10, self.screenHeight / 10, 0, 0),
            True
        )
        
        self.gameScreenComponents['Time'] = TextBox(
            AssetConstants.AMATICSC_FONT,
            ColorCodeTuples.WHITE,
            20,
            "Time",
            (self.screenWidth * 9 / 10, self.screenHeight / 10, 0, 0),
            True
        )
        
        self.gameScreenComponents['Watch'] = TextBox(
            AssetConstants.AMATICSC_FONT,
            ColorCodeTuples.WHITE,
            20,
            "Watcher:",
            (self.screenWidth * 9 / 10, self.screenHeight / 10 + 90, 0, 0),
            True
        )
        
        self.gameScreenComponents['Watcher'] = TextBox(
            AssetConstants.AMATICSC_FONT,
            ColorCodeTuples.WHITE,
            20,
            str(0),
            (self.screenWidth * 9 / 10, self.screenHeight / 10 + 120, 0, 0),
        )
        
        
        self.gameScreenComponents['Timer'] = TextBox(
            AssetConstants.AMATICSC_FONT,
            ColorCodeTuples.WHITE,
            20,
            str(self.timeLeft),
            (self.screenWidth * 9 / 10, self.screenHeight / 10 + 30, 0, 0),
        )

        self.openScreenComponents['playButton'] = Button(
            (self.screenWidth * 8 / 100, self.screenWidth * 8 / 100),
            AssetConstants.PLAY_BUTTON,
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

        self.bindSummaryUI()

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
        if self.openScreenComponents['nickname'].getText() == "":
            self.openScreenComponents['notify'].changeTextContent(MessageTextConstants.INVALID_MESSAGE_REGISTER)
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
                        self.client.requestNickname(self.nickname)
                        return
                self.openScreenComponents['notify'].changeTextContent("")
                self.openScreenComponents['nickname'].addText(event.unicode)
          
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mousePresses = pygame.mouse.get_pressed()
            elif pygame.VIDEORESIZE:
                pass

        startButtonState = self.openScreenComponents['playButton'].isClicked()

        if startButtonState:
            if self.validateNickname():
                self.nickname = self.openScreenComponents['nickname'].getText()
                self.client.requestNickname(self.nickname)
        
        self.screen.blit(self.backgroundImage, (0, 0))

        for element in self.openScreenComponents.values():
            element.draw(self.screen)
    
    def displayWaitScreen(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                return
        self.waitScreenComponents['notify'].changeTextContent(f'{self.summary['client_count_summary']['successfully_registered_player_count']}/{self.summary['client_count_summary']['required_number_of_players']}')
        self.screen.blit(self.inGameImage, (0, 0))
        
        for element in self.waitScreenComponents.values():
            element.draw(self.screen)

        pygame.display.update()
    
    def resetTimer(self):
        self.timeLeft = 20 - int(time.time() - self.summary["start_time"])
        self.submit = False
        self.gameScreenComponents['Timer'].changeTextContent(str(self.timeLeft))
        
        
    def displayMatchScreen(self):
        
        round = self.summary["round_count"]
        word = self.summary["quiz"]["current_keyword"]
        wordLength = len(word)
        hint_raw = self.summary["quiz"]["hint"]
        hint = "\n".join([hint_raw[i:i+30] for i in range(0, len(hint_raw), 30)])
        
        self.gameScreenComponents['hint'].changeTextContent(f"Hint: {hint}")
        self.gameScreenComponents['round'].changeTextContent(f"{self.nickname} - Round: {round}")
        self.myTurn = (self.summary["player"]["current_player"] == self.nickname)

        position = None
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                print("Mouse position: ", position)
            elif event.type == pygame.USEREVENT:
                if self.timeLeft > 0 and not self.submit:
                    self.timeLeft -= 1
                    self.gameScreenComponents['Timer'].changeTextContent(str(self.timeLeft))
        
        self.screen.blit(self.inGameImage, (0, 0))
        
        for element in self.gameScreenComponents.values():
            element.draw(self.screen)

        for button in self.buttons:
            
            button.draw(self.screen)
            
            if position and self.myTurn:
                
                if button.collision(position):
                    self.client.sendLetterGuess(button.text)
                    self.submit = True

        if self.timeLeft <= 0:
            if self.myTurn:
                self.client.sendLetterGuess(" ")
            self.submit = True
                

        for i in range(wordLength):
            x = self.screenWidth // 2 - ((18 * wordLength) // 2)
            x1, y1 = (x + 20 * i, self.screenHeight // 2)
            x2, y2 = (x + 20 * i + 15, self.screenHeight // 2)
            pygame.draw.line(self.screen, ColorCodeTuples.WHITE, (x1, y1), (x2, y2), 2)
            # draw the word
            text = self.font.render(word[i], True, ColorCodeTuples.WHITE)
            self.screen.blit(text, (x1 + 5, y1 - 20))
        
        playerInformation = self.summary["player"]["player_information"]
        currentPlayerNickname = self.summary["player"]["current_player"]

        for i, player in enumerate(playerInformation):
            self.scoreboard[i][0].drawLeftToRight(self.screen)
            self.scoreboard[i][1].drawLeftToRight(self.screen)
            if player["nickname"] == currentPlayerNickname: 
                self.scoreboard[i][0].changeColor(ColorCodeTuples.GREEN)
                self.scoreboard[i][1].changeColor(ColorCodeTuples.GREEN)
    
    def displayLoseScreen(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                return

        self.screen.blit(self.inGameImage, (0, 0))
        for element in self.loseScreenComponents.values():
            element.draw(self.screen)
        
    def displayStatisticScreen(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                return
       
        self.screen.blit(self.inGameImage, (0, 0))
        
        for element in self.statisticScreenComponents.values():
            element.draw(self.screen)
        
    def analyzeResponse(self) -> bool:
        response = self.client.getReceivedResponse()
        
        if response is None:
            return False

        statusCode = response.getStatusCode()
        content = response.getContent()

        if statusCode == ResponseStatusCode.BROADCASTED_SUMMARY:
            self.summary = json.loads(content)

            self.bindSummaryUI()

            print(f"[CLIENT] Received summary: {json.dumps(self.summary, indent = 4)}")
            
        elif statusCode == ResponseStatusCode.QUESTION_SENT:
            self.resetTimer()
            for button in self.buttons:
                if button.text in self.summary["guessed_characters"]:
                    button.updateColor()

        elif statusCode == ResponseStatusCode.BROADCASTED_RANK:
            self.ranks = json.loads(content)
            print(json.dumps(self.ranks, indent = 4))

        elif statusCode == ResponseStatusCode.NICKNAME_ACCEPTED:
            self.screenViewID = ScreenViewID.WAIT
            self.waitScreenComponents['hello'].changeTextContent(f"Hello, {self.nickname}!")
        elif statusCode == ResponseStatusCode.GAME_STARTED or statusCode == ResponseStatusCode.GAME_FULL:
            self.screenViewID = ScreenViewID.GAME
        

        return True

    def run(self):
        self.initialize()

        pygame.time.set_timer(pygame.USEREVENT, 1000)

        while self.running:
            self.clock.tick(self.information["frame_rate"])

            self.analyzeResponse()

            if self.screenViewID == ScreenViewID.REGISTER:
                self.displayRegisterScreen()
            elif self.screenViewID == ScreenViewID.WAIT:
                self.displayWaitScreen()
            elif self.screenViewID == ScreenViewID.GAME:
                self.displayMatchScreen()
            elif self.screenViewID == ScreenViewID.LOSE:
                self.displayLoseScreen()
            elif self.screenViewID == ScreenViewID.STATISTIC:
                self.displayStatisticScreen()
            
            if not self.running:
                break

            self.timeLeft = 20 - int(time.time() - self.summary["start_time"])
            self.gameScreenComponents["Timer"].changeTextContent(str(self.timeLeft))

            pygame.display.update()
        
        self.client.closeConnection()