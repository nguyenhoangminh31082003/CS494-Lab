import pygame
import Constant
import TextClass
import ButtonClass
import TextFormClass

class GUI:
    ScreenView = 0
    nickname = ""
    word = "***W**"
    score = 0
    round = 0
    turn = 0
    submit = False
    players_List = {
            "Lisa" : 10,
            "Ana" : 5,
            "John" : 0,
            "Doe" : 0,
        }
    timeLeft = 15

    open = {}
    wait = {}
    game = {}
    lose = {}
    stat = {}
    
    backgroundImage = None
    inGameImage = None
    running = False
    clock = None
    gameScreen = None
    screenWidth = None
    screenHeight = None
    
    btns = []
    players = []
    
    @staticmethod
    def initialize():
        pygame.init()
        pygame.display.set_caption(Constant.TITLE)
        infoObject = pygame.display.Info()
        screenSize = (infoObject.current_w * Constant.SCREEN_RATIO, infoObject.current_h * Constant.SCREEN_RATIO)
        GUI.gameScreen = pygame.display.set_mode(screenSize, pygame.RESIZABLE)
        GUI.screenWidth, GUI.screenHeight = screenSize
        # Run
        GUI.running = True
        GUI.clock = pygame.time.Clock()
        # Menu Background
        GUI.backgroundImage = pygame.transform.scale(Constant.MENU, (GUI.screenWidth, GUI.screenHeight))
        GUI.inGameImage = pygame.transform.scale(Constant.BACKGROUND, (GUI.screenWidth, GUI.screenHeight))

        # Content Box Container
        containerBoxContainer = (GUI.screenWidth * 350 / 1000, GUI.screenHeight * 170 / 563, GUI.screenWidth * 332 / 1000, GUI.screenHeight * 332 / 563)

        # Enter nickname
        GUI.open['label'] = TextClass.Text(
            Constant.AMATICSC_FONT,
            Constant.BLACK,
            32,
            Constant.ENTER_NICKNAME,
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

    @staticmethod
    def validateNickname():
        # duplicate
        
        # null
        if GUI.open['nickname'].getText() == "":
            GUI.open['notify'].changeTextContent(Constant.INVALID_MESSAGE_REGISTER)
            return False
        return True

    @staticmethod
    def resize():
                # Menu Background
        GUI.screenWidth, GUI.screenHeight = pygame.display.get_surface().get_size()
        GUI.backgroundImage = pygame.transform.scale(Constant.MENU, (GUI.screenWidth, GUI.screenHeight))

        # Content Box Container
        containerBoxContainer = (GUI.screenWidth * 350 / 1000, GUI.screenHeight * 170 / 563, GUI.screenWidth * 332 / 1000, GUI.screenHeight * 332 / 563)
        element_size = (GUI.screenWidth * 8 / 100, GUI.screenWidth * 8 / 100)
        for element in GUI.open.values():
            element.resize(containerBoxContainer, element_size)

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
    
    @staticmethod
    def run():
        GUI.initialize()
        pygame.time.set_timer(pygame.USEREVENT, 1000)
        while GUI.running:
            GUI.clock.tick(Constant.FPS)
            match GUI.ScreenView:
                case Constant.ScreenView.REGISTER:
                    GUI.registerScreen()
                case Constant.ScreenView.WAIT:
                    GUI.waitScreen()
                case Constant.ScreenView.GAME:
                    GUI.matchScreen()
                case Constant.ScreenView.LOSE:
                    GUI.loseScreen()
                case Constant.ScreenView.STAT:
                    GUI.statScreen()