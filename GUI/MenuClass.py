import pygame
import Constant
import TextClass
import ButtonClass



# enum for screen view
class ScreenView:
    REGISTER = 0
    WAIT = 1
    GAME = 2
    LOSE = 3
    STAT = 4

class Menu:
    def __init__(self, screenSize):
        pygame.init()

        ### Prepare data
        self.ScreenView = 1
        self.nickname = ""
        self.word = "***W**"
        self.score = 0
        self.round = 0
        self.turn = 0
        self.submit = False
        self.players_List = {
            "Lisa" : 10,
            "Ana" : 5,
            "John" : 0,
            "Doe" : 0,
        }
        self.timeLeft = 15
        
        # Menu Screen
        # allow screen size to be changed
        self.gameScreen = pygame.display.set_mode(screenSize, pygame.RESIZABLE)
        # when screen size is changed, scale the open
        
        self.screenWidth, self.screenHeight = pygame.display.get_surface().get_size()

        # Run
        self.running = True
        self.clock = pygame.time.Clock()

        self.open = {}
        self.wait = {}
        self.game = {}
        self.lose = {}
        self.stat = {}
        
        # Menu Background
        self.backgroundImage = pygame.transform.scale(Constant.MENU, (self.screenWidth, self.screenHeight))
        self.inGameImage = pygame.transform.scale(Constant.BACKGROUND, (self.screenWidth, self.screenHeight))

        # Content Box Container
        containerBoxContainer = (self.screenWidth * 350 / 1000, self.screenHeight * 170 / 563, self.screenWidth * 332 / 1000, self.screenHeight * 332 / 563)

        # Enter nickname
        self.open['label'] = TextClass.Text(
            Constant.AMATICSC_FONT,
            Constant.BLACK,
            32,
            Constant.ENTER_NICKNAME,
            (containerBoxContainer[0], containerBoxContainer[1] + containerBoxContainer[3] / 2, containerBoxContainer[2], containerBoxContainer[3] * 15 / 100)
        )
        
        self.wait['hello'] = TextClass.Text(
            Constant.AMATICSC_FONT,
            Constant.BLACK,
            32,
            "Hello, ",
            (containerBoxContainer[0], containerBoxContainer[1] + containerBoxContainer[3] / 2 - self.screenHeight * 20 / 100, containerBoxContainer[2], containerBoxContainer[3] * 15 / 100)
        )
        
        self.wait['label'] = TextClass.Text(
            Constant.AMATICSC_FONT,
            Constant.BLACK,
            32,
            Constant.PAUSE_TEXT,
            (containerBoxContainer[0], containerBoxContainer[1] + containerBoxContainer[3] / 2, containerBoxContainer[2], containerBoxContainer[3] * 15 / 100)
        )
        
        self.open['notify'] = TextClass.Text(
            Constant.AMATICSC_FONT,
            Constant.WHITE,
            20,
            "",
            (containerBoxContainer[0], containerBoxContainer[1] + containerBoxContainer[3] / 2 + self.screenHeight * 6 / 100, containerBoxContainer[2], containerBoxContainer[3] * 15 / 100)
        )
        
        self.wait['notify'] = TextClass.Text(
            Constant.AMATICSC_FONT,
            Constant.GREEN,
            16,
            "1/5",
            (containerBoxContainer[0], containerBoxContainer[1] + containerBoxContainer[3] / 2 + self.screenHeight * 10 / 100, containerBoxContainer[2], containerBoxContainer[3] * 15 / 100)
        )
        
        # Nickname TextForm
        self.open['nickname'] = TextClass.TextForm(
            Constant.AMATICSC_FONT,
            Constant.BLACK,
            20,
            (containerBoxContainer[0], containerBoxContainer[1] + containerBoxContainer[3] / 2 + self.screenHeight * 13 / 100, containerBoxContainer[2], containerBoxContainer[3] * 15 / 100)
        )
        
        self.btns = []
        for i in range(26):
            text = f"{chr(65+i)}"
            x = containerBoxContainer[0] - self.screenWidth * 1 / 10 + ( i % 9 ) * 36
            y = containerBoxContainer[1] + self.screenHeight * 28 / 100 + (i // 9) * 36
            self.btns.append(ButtonClass.TextButton(text, x, y))
        
        self.players = []
        for i in range(len(self.players_List)):
            player = list(self.players_List.keys())[i]
            score = list(self.players_List.values())[i]
            self.players.append((
                TextClass.Text(
                Constant.AMATICSC_FONT,
                Constant.WHITE,
                16,
                player,
                (self.screenWidth / 20, self.screenHeight / 10 + (i + 1) * 30, 0, 0),
            ),
              TextClass.Text(
                Constant.AMATICSC_FONT,
                Constant.WHITE,
                16,
                ": " + str(score),
                (self.screenWidth / 8, self.screenHeight / 10 + (i + 1) * 30, 0, 0),
            ))
                )
        
        self.game['round'] = TextClass.Text(
            Constant.AMATICSC_FONT,
            Constant.WHITE,
            30,
            "Round: 1",
            (containerBoxContainer[0], self.screenHeight / 10, containerBoxContainer[2], containerBoxContainer[3] * 15 / 100),
            True
        )
        
        self.game['player'] = TextClass.Text(
            Constant.AMATICSC_FONT,
            Constant.WHITE,
            20,
            "Players:",
            (self.screenWidth / 10, self.screenHeight / 10, 0, 0),
            True
        )
        
        self.game['Time'] = TextClass.Text(
            Constant.AMATICSC_FONT,
            Constant.WHITE,
            20,
            "Time",
            (self.screenWidth * 9 / 10, self.screenHeight / 10, 0, 0),
            True
        )
        
        self.game['Timer'] = TextClass.Text(
            Constant.AMATICSC_FONT,
            Constant.WHITE,
            20,
            str(self.timeLeft),
            (self.screenWidth * 9 / 10, self.screenHeight / 10 + 30, 0, 0),
        )

        # Start Button
        self.open['playButton'] = ButtonClass.Button(
            (self.screenWidth * 8 / 100, self.screenWidth * 8 / 100),
            Constant.PLAY_BUTTON,
            (containerBoxContainer[0], containerBoxContainer[1] + containerBoxContainer[3] / 2 + self.screenHeight * 25 / 100, containerBoxContainer[2], self.screenHeight - (containerBoxContainer[1] + containerBoxContainer[3]))
        )

    def validateNickname(self):
        # duplicate
        
        # null
        if self.open['nickname'].getText() == "":
            self.open['notify'].changeTextContent(Constant.INVALID_MESSAGE_REGISTER)
            return False
        return True

    def resize(self):
                # Menu Background
        self.screenWidth, self.screenHeight = pygame.display.get_surface().get_size()
        self.backgroundImage = pygame.transform.scale(Constant.MENU, (self.screenWidth, self.screenHeight))

        # Content Box Container
        containerBoxContainer = (self.screenWidth * 350 / 1000, self.screenHeight * 170 / 563, self.screenWidth * 332 / 1000, self.screenHeight * 332 / 563)
        element_size = (self.screenWidth * 8 / 100, self.screenWidth * 8 / 100)
        for element in self.open.values():
            element.resize(containerBoxContainer, element_size)

    def registerScreen(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.running = False
                    exit(0)
                case pygame.KEYDOWN:
                    # if the key is enter, validate the nickname
                    if event.key == pygame.K_RETURN:
                        if self.validateNickname():
                            self.nickname = self.open['nickname'].getText()
                            self.wait['hello'].changeTextContent("Hello, " + self.nickname + "!")
                            self.ScreenView = ScreenView.WAIT
                            return
                    self.open['notify'].changeTextContent("")
                    self.open['nickname'].addText(event.unicode)
                case pygame.MOUSEBUTTONDOWN:
                    mouse_presses = pygame.mouse.get_pressed()
                # when the screen is resized, scale the open
                case pygame.VIDEORESIZE:
                    # self.resize()
                    pass

        # Start Button Process
        startButtonState = self.open['playButton'].isClicked()

        if startButtonState == True:
            if self.validateNickname():
                self.nickname = self.open['nickname'].getText()
                self.wait['hello'].changeTextContent("Hello, " + self.nickname + "!")
                self.ScreenView = ScreenView.WAIT
        # Draw Window
        self.gameScreen.blit(self.backgroundImage, (0, 0))
        for element in self.open.values():
            element.draw(self.gameScreen)
        pygame.display.update()
    
    def waitScreen(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.running = False
                    exit(0)
                case pygame.MOUSEBUTTONDOWN:
                    self.ScreenView = ScreenView.GAME
        self.gameScreen.blit(self.inGameImage, (0, 0))
        for element in self.wait.values():
            element.draw(self.gameScreen)
        pygame.display.update()
        
    
    def matchScreen(self):
        pos = None
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.running = False
                    exit(0)
                case pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                case pygame.USEREVENT:
                    if self.timeLeft and not self.submit:
                        self.timeLeft -= 1
                        self.game['Timer'].changeTextContent(str(self.timeLeft))
        self.gameScreen.blit(self.inGameImage, (0, 0))
        for element in self.game.values():
            element.draw(self.gameScreen)
        for btn in self.btns:
            btn.draw(self.gameScreen)
            if pos:
                if btn.collision(pos):
                    self.submit = True
        if self.timeLeft == 0:
            self.submit = True
        for i in range(len(self.word)):
            x = self.screenWidth // 2 - ((18 * len(self.word)) // 2)
            x1, y1 = (x + 20 * i,self.screenHeight // 2)
            x2, y2 = (x + 20 * i + 15, self.screenHeight // 2)
            pygame.draw.line(self.gameScreen, Constant.WHITE, (x1, y1), (x2, y2), 2)
        for i in range(len(self.players_List)):
            self.players[i][0].drawLeftToRight(self.gameScreen)
            self.players[i][1].drawLeftToRight(self.gameScreen)
            if i == self.turn: 
                self.players[i][0].changeColor(Constant.GREEN)
                self.players[i][1].changeColor(Constant.GREEN)
        pygame.display.update()
    
    def loseScreen(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.running = False
                    exit(0)
        self.gameScreen.blit(self.inGameImage, (0, 0))
        for element in self.lose.values():
            element.draw(self.gameScreen)
        pygame.display.update()
    
    def statScreen(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.running = False
                    exit(0)
        self.gameScreen.blit(self.inGameImage, (0, 0))
        for element in self.stat.values():
            element.draw(self.gameScreen)
        pygame.display.update()
    
    def run(self):
        pygame.time.set_timer(pygame.USEREVENT, 1000)
        while self.running:
            self.clock.tick(Constant.FPS)
            match self.ScreenView:
                case ScreenView.REGISTER:
                    self.registerScreen()
                case ScreenView.WAIT:
                    self.waitScreen()
                case ScreenView.GAME:
                    self.matchScreen()
                case ScreenView.LOSE:
                    self.loseScreen()
                case ScreenView.STAT:
                    self.statScreen()