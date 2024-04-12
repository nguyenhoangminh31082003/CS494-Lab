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
        self.keyword_button = None 
        self.keyword_textform = None
        self.guess_keyword = False
        self.client = client
        self.scoreboard = []
        self.statistic = []

        self.summary = None

        self.timeLeft = 20
        self.nickname = None
        self.rankSummary = None
        self.restartAllowance = False
        
    def bindStatisticUI(self) -> bool:
        
        if self.rankSummary is None:
            return False
        
        self.statistic.clear()
        keyword = self.rankSummary["quiz_summary"]["current_keyword"].upper()
        rankInformation = self.rankSummary['rank_summary']["ranks"]
        
        self.statisticScreenComponents['keyword'].changeTextContent(f"ANSWER: {keyword}")
        
        for i, rank in enumerate(rankInformation):
            self.statistic.append(
                (
                    TextBox(
                        textFont = AssetConstants.AMATICSC_FONT,
                        textColor = ColorCodeTuples.WHITE,
                        textSize = 16,
                        textContent = f"{rank["rank"]}",
                        containerInfo = (
                            self.screenWidth / 2 - 100, 
                            self.screenHeight / 3 + (i + 1) * 30, 0, 0
                        )
                    ),
                    TextBox(
                        textFont = AssetConstants.AMATICSC_FONT,
                        textColor = ColorCodeTuples.WHITE,
                        textSize = 16,
                        textContent = rank["nickname"],
                        containerInfo = (
                            self.screenWidth / 2 - 60, 
                            self.screenHeight / 3 + (i + 1) * 30, 0, 0
                        )
                    ),
                    TextBox(
                        textFont = AssetConstants.AMATICSC_FONT,
                        textColor = ColorCodeTuples.WHITE,
                        textSize = 16,
                        textContent = f": {rank['points']}",
                        containerInfo = (
                            self.screenWidth / 2 + 100, 
                            self.screenHeight / 3 + (i + 1) * 30, 0, 0
                        ),
                    )
                )
            )
        
        if self.nickname in self.rankSummary['rank_summary']['winner_nicknames']:
            self.statisticScreenComponents['label'].changeTextContent(MessageTextConstants.WIN_TEXT)
         
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
                        textSize = 12,
                        textContent = str(player["order"]),
                        containerInfo = (
                            10, 
                            self.screenHeight / 10 + 90 + (i + 1) * 30, 0, 0
                        )
                    ),
                    TextBox(
                        textFont = AssetConstants.AMATICSC_FONT,
                        textColor = color,
                        textSize = 12,
                        textContent = player["nickname"],
                        containerInfo = (
                            self.screenWidth / 7 - 60, 
                            self.screenHeight / 10 + 90 + (i + 1) * 30, 0, 0
                        )
                    ),
                    TextBox(
                        textFont = AssetConstants.AMATICSC_FONT,
                        textColor = color,
                        textSize = 12,
                        textContent = f": {player['points']}",
                        containerInfo = (
                            self.screenWidth / 7 + 20, 
                            self.screenHeight / 10 + 90 + (i + 1) * 30, 0, 0
                        ),
                    )
                )
            )

        watcher = self.summary["client_count_summary"]["watcher_count"]
        self.gameScreenComponents['Watcher'].changeTextContent(str(watcher))
        self.timeLeft = 20 - int(time.time() - self.summary["start_time"])
        self.gameScreenComponents['Timer'].changeTextContent(str(self.timeLeft))
        
        return True
    
    def initializeKeyboard(self):
        containerBoxContainer = (
            self.screenWidth * 350 / 1000, 
            self.screenHeight * 170 / 563, 
            self.screenWidth * 332 / 1000, 
            self.screenHeight * 332 / 563
        )

        self.buttons.clear()

        for i in range(26):
            text = f"{chr(65 + i)}"
            x = containerBoxContainer[0] - self.screenWidth * 1 / 10 + ( i % 9 ) * 36
            y = containerBoxContainer[1] + self.screenHeight * 28 / 100 + (i // 9) * 36
            self.buttons.append(TextButton(text, x, y))

    def initializeScreenComponents(self):
        containerBoxContainer = (
            self.screenWidth * 350 / 1000, 
            self.screenHeight * 170 / 563, 
            self.screenWidth * 332 / 1000, 
            self.screenHeight * 332 / 563
        )
        
        self.statisticScreenComponents['RESTART'] = TextBox(
            AssetConstants.AMATICSC_FONT,
            ColorCodeTuples.WHITE,
            20,
            "RESTART",
            (containerBoxContainer[0], containerBoxContainer[1] + containerBoxContainer[3] / 2 + self.screenHeight * 13 / 100, containerBoxContainer[2], containerBoxContainer[3] * 15 / 100),
            True
        )
        
        self.font = pygame.font.Font(AssetConstants.AMATICSC_FONT, 20)

        self.openScreenComponents['label'] = TextBox(
            textFont = AssetConstants.AMATICSC_FONT,
            textColor = ColorCodeTuples.BLACK,
            textSize = 32,
            textContent = MessageTextConstants.ENTER_NICKNAME,
            containerInfo = (containerBoxContainer[0], containerBoxContainer[1] + containerBoxContainer[3] / 2, containerBoxContainer[2], containerBoxContainer[3] * 15 / 100)
        )
        
        self.waitScreenComponents['hello'] = TextBox(
            textFont = AssetConstants.AMATICSC_FONT,
            textColor = ColorCodeTuples.WHITE,
            textSize = 32,
            textContent = "Hello, ",
            containerInfo = (containerBoxContainer[0], containerBoxContainer[1] + containerBoxContainer[3] / 2 - self.screenHeight * 20 / 100, containerBoxContainer[2], containerBoxContainer[3] * 15 / 100)
        )
        
        self.waitScreenComponents['label'] = TextBox(
            textFont = AssetConstants.AMATICSC_FONT,
            textColor = ColorCodeTuples.WHITE,
            textSize = 32,
            textContent = MessageTextConstants.PAUSE_TEXT,
            containerInfo = (containerBoxContainer[0], containerBoxContainer[1] + containerBoxContainer[3] / 2, containerBoxContainer[2], containerBoxContainer[3] * 15 / 100)
        )
        
        self.statisticScreenComponents['label'] = TextBox(
            textFont = AssetConstants.AMATICSC_FONT,
            textColor = ColorCodeTuples.WHITE,
            textSize = 32,
            textContent = MessageTextConstants.END_TEXT,
            containerInfo = (containerBoxContainer[0], self.screenHeight / 10, containerBoxContainer[2], containerBoxContainer[3] * 15 / 100)
        )
        
        self.statisticScreenComponents['keyword'] = TextBox(
            textFont = AssetConstants.AMATICSC_FONT,
            textColor = ColorCodeTuples.WHITE,
            textSize = 20,
            textContent = "ANSWER",
            containerInfo = (containerBoxContainer[0], self.screenHeight * 2 / 10, containerBoxContainer[2], containerBoxContainer[3] * 15 / 100)
        )
        
        self.openScreenComponents['notify'] = TextBox(
            textFont = AssetConstants.AMATICSC_FONT,
            textColor = ColorCodeTuples.WHITE,
            textSize = 20,
            textContent = str(),
            containerInfo = (containerBoxContainer[0], containerBoxContainer[1] + containerBoxContainer[3] / 2 + self.screenHeight * 6 / 100, containerBoxContainer[2], containerBoxContainer[3] * 15 / 100)
        )
        
        self.waitScreenComponents['notify'] = TextBox(
            textFont = AssetConstants.AMATICSC_FONT,
            textColor = ColorCodeTuples.GREEN,
            textSize = 12,
            textContent = "1/5",
            containerInfo = (containerBoxContainer[0], containerBoxContainer[1] + containerBoxContainer[3] / 2 + self.screenHeight * 10 / 100, containerBoxContainer[2], containerBoxContainer[3] * 15 / 100)
        )
        
        # Nickname TextForm
        self.openScreenComponents['nickname'] = TextForm(
            textFont = AssetConstants.AMATICSC_FONT,
            textColor = ColorCodeTuples.BLACK,
            textSize = 20,
            containerInfo = (containerBoxContainer[0], containerBoxContainer[1] + containerBoxContainer[3] / 2 + self.screenHeight * 13 / 100, containerBoxContainer[2], containerBoxContainer[3] * 15 / 100)
        )
        
        self.gameScreenComponents['round'] = TextBox(
            textFont = AssetConstants.AMATICSC_FONT,
            textColor = ColorCodeTuples.WHITE,
            textSize = 30,
            textContent = "abcxyzfgkh - Round: 1",
            containerInfo = (containerBoxContainer[0], self.screenHeight / 10, containerBoxContainer[2], containerBoxContainer[3] * 15 / 100),
            border = True
        )
        
        self.gameScreenComponents['hint'] = TextBox(
            textFont = AssetConstants.AMATICSC_FONT,
            textColor = ColorCodeTuples.WHITE,
            textSize = 12,
            textContent = "hint",
            containerInfo = (containerBoxContainer[0], self.screenHeight * 2 / 10, containerBoxContainer[2], containerBoxContainer[3] * 15 / 100),
        )
        
        self.gameScreenComponents['player'] = TextBox(
            textFont = AssetConstants.AMATICSC_FONT,
            textColor = ColorCodeTuples.WHITE,
            textSize = 20,
            textContent = "Players:",
            containerInfo = (self.screenWidth / 10, self.screenHeight / 10 + 90, 0, 0),
            border = True
        )
        
        self.gameScreenComponents['Time'] = TextBox(
            textFont = AssetConstants.AMATICSC_FONT,
            textColor = ColorCodeTuples.WHITE,
            textSize = 20,
            textContent = "Time",
            containerInfo = (self.screenWidth * 9 / 10, self.screenHeight / 10, 0, 0),
            border = True
        )
        
        self.gameScreenComponents['Watch'] = TextBox(
            textFont = AssetConstants.AMATICSC_FONT,
            textColor = ColorCodeTuples.WHITE,
            textSize = 20,
            textContent = "Watcher:",
            containerInfo = (self.screenWidth * 9 / 10, self.screenHeight / 10 + 90, 0, 0),
            border = True
        )
        
        self.gameScreenComponents['Watcher'] = TextBox(
            textFont = AssetConstants.AMATICSC_FONT,
            textColor = ColorCodeTuples.WHITE,
            textSize = 20,
            textContent = str(0),
            containerInfo = (self.screenWidth * 9 / 10, self.screenHeight / 10 + 120, 0, 0),
        )
        
        self.gameScreenComponents['Timer'] = TextBox(
            textFont = AssetConstants.AMATICSC_FONT,
            textColor = ColorCodeTuples.WHITE,
            textSize = 20,
            textContent = str(self.timeLeft),
            containerInfo = (self.screenWidth * 9 / 10, self.screenHeight / 10 + 30, 0, 0),
        )

        self.openScreenComponents['playButton'] = Button(
            (self.screenWidth * 8 / 100, self.screenWidth * 8 / 100),
            AssetConstants.PLAY_BUTTON,
            (containerBoxContainer[0], containerBoxContainer[1] + containerBoxContainer[3] / 2 + self.screenHeight * 25 / 100, containerBoxContainer[2], self.screenHeight - (containerBoxContainer[1] + containerBoxContainer[3]))
        )
        
        self.keyword_button = TextBox(
            textFont = AssetConstants.AMATICSC_FONT,
            textColor = ColorCodeTuples.WHITE,
            textSize = 20,
            textContent = "KEYWORD",
            containerInfo = (containerBoxContainer[0] - self.screenWidth * 1 / 10 + ( 26 % 9 ) * 36 + 60, containerBoxContainer[1] + self.screenHeight * 28 / 100 + (26 // 9) * 36 + 14, 0, 0),
            border = True
        )
        
        self.keyword_textform = TextForm(
            textFont = AssetConstants.AMATICSC_FONT,
            textColor = ColorCodeTuples.BLACK,
            textSize = 20,
            containerInfo = (containerBoxContainer[0], containerBoxContainer[1] + self.screenHeight * 50 / 100, containerBoxContainer[2], containerBoxContainer[3] * 15 / 100),
            maxChar = 30
        )
            
    def initializeImages(self):
        self.backgroundImage = pygame.transform.scale(
            AssetConstants.INTRO, 
            (
                self.screenWidth, 
                self.screenHeight
            )
        )

        self.inGameImage = pygame.transform.scale(
            AssetConstants.INGAME, 
            (
                self.screenWidth, 
                self.screenHeight
            )
        )
        
        self.statImage = pygame.transform.scale(
            AssetConstants.CHEST, 
            (
                self.screenWidth, 
                self.screenHeight
            )
        )

    def initialize(self):
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
        self.keyword_button = None 
        self.keyword_textform = None
        self.guess_keyword = False
        self.scoreboard = []
        self.statistic = []

        self.summary = None

        self.timeLeft = 20
        self.rankSummary = None
        
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

        self.initializeKeyboard()

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
        
        round = self.summary["round_count"] + 1
        word = self.summary["quiz"]["current_keyword"].upper()
        wordLength = len(word)
        hint = self.summary["quiz"]["hint"]
        order = self.summary['turn_count'] + 1
        
        
        self.gameScreenComponents['hint'].changeTextContent(f"Hint: {hint}")
        self.gameScreenComponents['round'].changeTextContent(f"{self.nickname} - Round: {round}")
        self.myTurn = (self.summary["player"]["current_player"] == self.nickname)

        position = None
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if self.keyword_textform.checkSelection():
                    if event.key == pygame.K_RETURN:
                        if self.keyword_textform.checkSelection():
                            self.client.sendWordGuess(self.keyword_textform.getText())
                            self.keyword_textform.alterSelection()
                    self.keyword_textform.addText(event.unicode)
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
            
            if position and self.myTurn and not self.keyword_textform.checkSelection():
                
                if button.collision(position):
                    self.client.sendLetterGuess(button.text)
                    self.submit = True

        if self.timeLeft <= 0:
            if self.myTurn:
                self.client.sendLetterGuess(" ")
            self.submit = True
            
        if position and self.myTurn and order > 2:
            if self.keyword_button.isClicked(position):
                self.keyword_textform.alterSelection()
                

        for i in range(wordLength):
            x = self.screenWidth // 2 - ((18 * wordLength) // 2)
            x1, y1 = (x + 20 * i, self.screenHeight // 2)
            x2, y2 = (x + 20 * i + 15, self.screenHeight // 2)
            pygame.draw.line(self.screen, ColorCodeTuples.WHITE, (x1, y1), (x2, y2), 2)
            # draw the word
            text = self.font.render(word[i], True, ColorCodeTuples.WHITE)
            self.screen.blit(text, (x1 - text.get_width() / 2 + 10, y1 - 30))
        
        playerInformation = self.summary["player"]["player_information"]
        currentPlayerNickname = self.summary["player"]["current_player"]
        self.keyword_button.draw(self.screen)

        for i, player in enumerate(playerInformation):
            self.scoreboard[i][0].drawLeftToRight(self.screen)
            self.scoreboard[i][1].drawLeftToRight(self.screen)
            self.scoreboard[i][2].drawLeftToRight(self.screen)
            if player["nickname"] == currentPlayerNickname: 
                self.scoreboard[i][0].changeColor(ColorCodeTuples.GREEN)
                self.scoreboard[i][1].changeColor(ColorCodeTuples.GREEN)
                self.scoreboard[i][2].changeColor(ColorCodeTuples.GREEN)
            if player['alive'] == False:
                self.scoreboard[i][0].changeColor(ColorCodeTuples.RED)
                self.scoreboard[i][1].changeColor(ColorCodeTuples.RED)
                self.scoreboard[i][2].changeColor(ColorCodeTuples.RED)
        
        if self.keyword_textform.checkSelection():
            self.keyword_textform.draw(self.screen)
    
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
        pos = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
        
        self.screen.blit(self.statImage, (0, 0))
        
        if pos and self.statisticScreenComponents['RESTART'].isClicked(pos) and self.restartAllowance:
            self.client.requestRestartNewMatch()
        
        for element in self.statisticScreenComponents.values():
            element.draw(self.screen)
        
        for stat in self.statistic:
            stat[0].draw(self.screen)
            stat[1].draw(self.screen)
            stat[2].draw(self.screen)
            if stat[1].textContent == self.nickname:
                stat[0].changeColor(ColorCodeTuples.GREEN)
                stat[1].changeColor(ColorCodeTuples.GREEN)
                stat[2].changeColor(ColorCodeTuples.GREEN)
        
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
            
        elif statusCode == ResponseStatusCode.BROADCASTED_RANK:
            self.rankSummary = json.loads(content)
            self.bindStatisticUI()
            self.screenViewID = ScreenViewID.STATISTIC
            
        elif statusCode == ResponseStatusCode.QUESTION_SENT:
            self.resetTimer()
            for button in self.buttons:
                if button.text in self.summary["guessed_characters"]:
                    button.updateColor()

        elif statusCode == ResponseStatusCode.NICKNAME_ACCEPTED:
            self.screenViewID = ScreenViewID.WAIT
            self.waitScreenComponents['hello'].changeTextContent(f"Hello, {self.nickname}!")
        elif statusCode == ResponseStatusCode.WAIT_GAME_START_REQUIRED:
            self.restartAllowance = False
            self.screenViewID = ScreenViewID.WAIT
            self.waitScreenComponents['hello'].changeTextContent(f"Hello, {self.nickname}!")
            self.initializeScreenComponents()
        elif statusCode == ResponseStatusCode.GAME_FULL:
            self.nickname = "Watcher"   
            
            started = json.loads(content)["game_started"]
            
            if started:
                self.screenViewID = ScreenViewID.GAME
            else:
                self.screenViewID = ScreenViewID.WAIT
                self.waitScreenComponents['hello'].changeTextContent(f"Hello, {self.nickname}!")
                
        elif statusCode == ResponseStatusCode.GAME_STARTED:
            self.screenViewID = ScreenViewID.GAME
        elif statusCode == ResponseStatusCode.RESTART_ALLOWED:
            self.restartAllowance = True
            self.initializeKeyboard()

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