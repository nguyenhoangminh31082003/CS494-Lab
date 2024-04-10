import pygame
import threading
import sys

sys.path.append('./Game/')

from Constant import *

class GUI:
    background = pygame.transform.scale(pygame.image.load(MENU), (WIDTH, HEIGHT))
    user_text = ''
    run = None
    state = None
    output = ''
    processing_output = False
    error_message = None
    model = None
    count_down_time = 10
    done_count = False
    result_list = None

    @staticmethod
    def set_count_down(amount):
        GUI.count_down_time = amount

    @staticmethod
    def is_alive():
        return GUI.run

    @staticmethod
    def draw_background(win):
        win.blit(GUI.background, (0, 0))

    @staticmethod
    def flip_cursor(win, size, pos, cursorPos=-1, flip=False):
        for col in range(size):
            if flip and col == cursorPos:
                continue
            pygame.draw.rect(win, WHITE, (pos[0] + col * LINE_SIZE, pos[1], LINE_SIZE - LINE_DISTANCE, LINE_THICK))

    @staticmethod
    def draw_title_at(win, base_font, title, color, pos):
        if title is None:
            return
        text = base_font.render(title, True, color)
        win.blit(text, (pos[0], pos[1]))

    @staticmethod
    def draw_text_at(win, user_text, base_font, pos):
        for col in range(len(user_text)):
            text = base_font.render(user_text[col], True, WHITE)
            win.blit(text, (pos[0] + col * LINE_SIZE, pos[1]))


    @staticmethod
    def get_output_from_state(state, error_message=None, model=None, result_list=None):
        if GUI.run == False:
            return 'SYSCLOSESYS'

        while GUI.state is not None:
            pygame.time.wait(100)

        GUI.error_message = error_message
        GUI.model = model
        GUI.result_list = result_list
        GUI.state = state

        while GUI.state is not None:
            if GUI.run == False:
                return 'SYSCLOSESYS'
            pygame.time.wait(100)
        if len(GUI.output) ==0:
            GUI.output = BLANK_WORD
        return GUI.output

    @staticmethod
    def pause(win, base_font, clock):
        GUI.state = None
        if not GUI.run:
            return

        GUI.pause_screen(win, base_font)
        pygame.display.update()
        while GUI.state is None:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    GUI.run = False
                    return

    @staticmethod
    def count_down():
        while GUI.count_down_time > 0 and not GUI.done_count:
            pygame.time.delay(1000)
            GUI.count_down_time -= 1


    @staticmethod
    def game_loop():
        pygame.init()
        WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Magical Wheel')
        base_font = pygame.font.SysFont("Time New Roman, Arial", TEXT_SIZE)
        small_font = pygame.font.SysFont("Time New Roman, Arial", 20)

        GUI.run = True
        clock = pygame.time.Clock()

        while GUI.run:
            if GUI.state == STATE_COMPLETE_REGISTER:
                GUI.register_successful_screen(WIN, base_font)
            elif GUI.state == STATE_VIEW_RESULT:
                GUI.result_screen(WIN, base_font, GUI.result_list)
            elif GUI.state == STATE_END:
                GUI.end_screen(WIN, base_font)
                # GUI.run = False
            elif GUI.state is not None:
                GUI.play_screen(WIN, base_font, clock, GUI.state, GUI.model, small_font)
            GUI.pause(WIN, base_font, clock)
        print('GUI thread end')
        pygame.quit()

    @staticmethod
    def register_successful_screen(win, base_font):
        GUI.output = ''
        GUI.draw_background(win)
        GUI.draw_title_at(win, base_font, 'Registration Completed Successfully!', AQUA, (WIDTH / 4, HEIGHT / 2 - TEXT_SIZE * 3))

    @staticmethod
    def result_screen(win, base_font, result_list=None):
        GUI.output = ''
        GUI.draw_background(win)
        GUI.draw_title_at(win, base_font, 'Player', AQUA,
                          (WIDTH / 4, HEIGHT / 4 - 4))
        GUI.draw_title_at(win, base_font, 'Rank', AQUA,
                          (WIDTH / 2, HEIGHT / 4 - 4))
        GUI.draw_title_at(win, base_font, 'Point', AQUA,
                          (3 * WIDTH / 4, HEIGHT / 4 - 4))

        pygame.draw.rect(win, PINK, (WIDTH / 4, HEIGHT / 4 + TEXT_SIZE, len('Point') * 12 + WIDTH / 2, LINE_THICK))
        if result_list is None:
            return
        line = 1
        for value in result_list:
            eR = 0
            eP = 0
            temp = int(line)
            while (temp // 10) != 0:
                temp //= 10
                eR += 12

            temp = int(value[1])
            while (temp // 10) != 0:
                temp //= 10
                eP += 12
                
            GUI.draw_title_at(win, base_font, str(value[0]), WHITE,
                              (WIDTH / 4, HEIGHT / 4 + line * TEXT_SIZE))
            GUI.draw_title_at(win, base_font, str(line), WHITE,
                              (WIDTH / 2 + LINE_SIZE - eR, HEIGHT / 4 + line * TEXT_SIZE))
            GUI.draw_title_at(win, base_font, str(value[1]), WHITE,
                              (3 * WIDTH / 4 + LINE_SIZE - eP, HEIGHT / 4 + line * TEXT_SIZE))
            line += 1

    @staticmethod
    def result_screen_small(win, base_font, result_list=None):
        GUI.output = ''

        shape_surf = pygame.Surface(pygame.Rect((17 * WIDTH / 20 + 4, TEXT_SIZE * 3 + 1, WIDTH, 20 * 12)).size,
                                    pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, (0, 0, 0, 128), shape_surf.get_rect())
        win.blit(shape_surf, (17 * WIDTH / 20 + 4, TEXT_SIZE * 3 + 4, WIDTH, 20 * 11))

        GUI.draw_title_at(win, base_font, 'Rank', AQUA,
                          (17*WIDTH/20 + 10, TEXT_SIZE * 3 + 5))
        GUI.draw_title_at(win, base_font, 'Player', AQUA,
                          (18*WIDTH/20 + 10, TEXT_SIZE * 3 + 5))
        GUI.draw_title_at(win, base_font, 'Point', AQUA,
                          (19*WIDTH/20 + 10, TEXT_SIZE * 3 + 5))

        #pygame.draw.rect(win, PINK, (8 * WIDTH / 10, TEXT_SIZE * 3 + TEXT_SIZE, len('Point') * 12 + WIDTH / 2, LINE_THICK))
        if result_list is None:
            return
        line = 1
        for value in result_list:
            eR = 0
            eP = 0
            temp = int(line)
            while (temp // 10) != 0:
                temp //= 10
                eR += 12

            temp = int(value[1])
            while (temp // 10) != 0:
                temp //= 10
                eP += 12
                
            GUI.draw_title_at(win, base_font, str(value[0]), WHITE,
                              (18*WIDTH/20, TEXT_SIZE * 3 + 10 + line * 20))
            GUI.draw_title_at(win, base_font, str(line), WHITE,
                              (17*WIDTH/20 + LINE_SIZE - eR, TEXT_SIZE * 3 + 10 + line * 20))
            GUI.draw_title_at(win, base_font, str(value[1]), WHITE,
                              (19*WIDTH/20 + LINE_SIZE - eP, TEXT_SIZE * 3 + 10 + line * 20 ))
            line += 1

    @staticmethod
    def pause_screen(win, base_font):
        CENTER_X = WIDTH - len(PAUSE_TEXT)*AVG_TEXT_SIZE*1.3
        CENTER_Y = 0

        text = base_font.render(PAUSE_TEXT, True, WHITE)
        win.blit(text, (CENTER_X, CENTER_Y))

    @staticmethod
    def end_screen(win, base_font):
        CENTER_X = (WIDTH - len(END_TEXT) * AVG_TEXT_SIZE) /2
        CENTER_Y = HEIGHT /2

        GUI.draw_background(win)
        # text = base_font.render(END_TEXT, True, WHITE)
        # win.blit(text, (CENTER_X, CENTER_Y))

        GUI.draw_text_at(win, END_TEXT, base_font,
                         (CENTER_X, CENTER_Y))


    @staticmethod
    def play_screen(WIN, base_font, clock, screen_mode, model=None, small_font=None):
        if screen_mode in (STATE_PLAY_LETTER, STATE_PLAY_WORD, STATE_WAIT):
            if model is None:
                GUI.output = ''
                return


        cursorPos = len(GUI.user_text)
        flipCursor = False

        GUI.done_count = False
        t = threading.Thread(target=GUI.count_down)
        input_size = 1
        if screen_mode == STATE_REGISTER:
            input_size = MAX_NICKNAME
        else:
            if screen_mode == STATE_PLAY_WORD:
                input_size = len(model.keyword)
            if screen_mode != STATE_WAIT_WITHOUT_COUNT:
                t.start()

        while True:
            clock.tick(FPS)

            if screen_mode != STATE_REGISTER and screen_mode != STATE_WAIT_WITHOUT_COUNT:
                if GUI.count_down_time == 0:
                    GUI.output = GUI.user_text
                    GUI.user_text = ''
                    GUI.done_count = True
                    t.join()
                    return

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    GUI.run = False
                    GUI.output = 'SYSCLOSESYS'
                    if screen_mode != STATE_REGISTER  and screen_mode != STATE_WAIT_WITHOUT_COUNT:
                        GUI.done_count = True
                        t.join()
                    return

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        GUI.output = GUI.user_text
                        GUI.user_text = ''
                        if screen_mode != STATE_REGISTER and screen_mode != STATE_WAIT_WITHOUT_COUNT:
                            GUI.done_count = True
                            t.join()
                        return

                    elif event.key == pygame.K_BACKSPACE:
                        GUI.user_text = GUI.user_text[:-1]
                        if cursorPos > 0:
                            cursorPos -= 1
                    elif len(GUI.user_text) < input_size:
                        GUI.user_text += event.unicode
                        if event.unicode:
                            cursorPos += 1

            #Drawing
            GUI.draw_switch(WIN, base_font, cursorPos, flipCursor, screen_mode, input_size, model, small_font)

            pygame.display.update()
            flipCursor = not flipCursor
            pygame.time.wait(100)

            if screen_mode == STATE_WAIT_WITHOUT_COUNT :
                return

    @staticmethod
    def draw_switch(WIN, base_font, cursorPos, flipCursor, screen_mode, input_size, model=None, small_font=None):
        GUI.draw_background(WIN)

        if screen_mode == STATE_REGISTER:
            GUI.flip_cursor(WIN, input_size,
                            ((WIDTH - input_size * LINE_SIZE) / 2, HEIGHT / 2), cursorPos, flipCursor)
            GUI.draw_title_at(WIN, base_font, ENTER_NICKNAME, WHITE, (WIDTH / 4, HEIGHT / 2 - TEXT_SIZE * 3))
            GUI.draw_title_at(WIN, base_font, GUI.error_message, RED, (WIDTH / 4, HEIGHT / 2 - TEXT_SIZE * 5))
            GUI.draw_text_at(WIN, GUI.user_text, base_font,
                             ((WIDTH - input_size * LINE_SIZE) / 2 + LINE_DISTANCE / 2, HEIGHT / 2 - TEXT_SIZE))
        else:
            GUI.draw_title_at(WIN, base_font, 'Player: ' + model.nickname, WHITE, (0, 0))
            GUI.draw_title_at(WIN, base_font, 'Order: ' + str(model.id), WHITE, (WIDTH / 3, 0))
            GUI.draw_title_at(WIN, base_font, 'Total: ' + str(model.total), WHITE, (WIDTH / 2, 0))
            GUI.draw_title_at(WIN, base_font, 'Turn: ' + str(model.gameTurn), WHITE, (2 * WIDTH / 3, 0))
            GUI.draw_title_at(WIN, base_font, 'Point: ' + str(model.point), WHITE, (0, TEXT_SIZE))
            GUI.draw_title_at(WIN, base_font, 'Rank: ' + str(model.rank), WHITE, (WIDTH / 3, TEXT_SIZE))
            GUI.draw_title_at(WIN, base_font, 'Player ' + str(model.currentPlayingPlayerID) + ' is playing', WHITE,
                              (0, TEXT_SIZE * 2 + 1))

            GUI.result_screen_small(WIN, small_font, GUI.result_list)

            if screen_mode != STATE_WAIT_WITHOUT_COUNT:
                # Count down
                GUI.draw_title_at(WIN, base_font, str(GUI.count_down_time), WHITE,
                                  (WIDTH - len(str(GUI.count_down_time)) * AVG_TEXT_SIZE * 2, TEXT_SIZE * 2 + 1))


            # Word
            GUI.draw_text_at(WIN, model.keyword, base_font,
                             ((WIDTH - len(model.keyword) * LINE_SIZE) / 2 + LINE_DISTANCE / 2,
                              HEIGHT / 2 - TEXT_SIZE))
            GUI.flip_cursor(WIN, len(model.keyword),
                            ((WIDTH - len(model.keyword) * LINE_SIZE) / 2, HEIGHT / 2))
            GUI.draw_title_at(WIN, base_font, model.description, WHITE,
                              ((WIDTH - len(model.description) * AVG_TEXT_SIZE) / 2, (HEIGHT + TEXT_SIZE) / 2))

            if screen_mode == STATE_PLAY_LETTER:
                # Enter Letter
                GUI.draw_title_at(WIN, base_font, 'Guess letter:', WHITE, (0, 3 * HEIGHT / 4))
                GUI.flip_cursor(WIN, input_size,
                                (len('Guess letter:') * AVG_TEXT_SIZE*1.2, TEXT_SIZE + 3 * HEIGHT / 4), cursorPos, flipCursor)
                GUI.draw_text_at(WIN, GUI.user_text, base_font,
                                 (len('Guess letter:') * AVG_TEXT_SIZE*1.2, 3 * HEIGHT / 4))
            elif screen_mode == STATE_PLAY_WORD:
                # Enter Letter
                GUI.draw_title_at(WIN, base_font, 'Letter choice:', WHITE, (0, 3 * HEIGHT / 4))
                GUI.flip_cursor(WIN, 1,
                                (len('Letter choice:') * AVG_TEXT_SIZE*1.2, TEXT_SIZE + 3 * HEIGHT / 4))
                GUI.draw_text_at(WIN, model.guessLetter, base_font,
                                 (len('Letter choice:') * AVG_TEXT_SIZE*1.2, 3 * HEIGHT / 4))

                # Enter word
                GUI.draw_title_at(WIN, base_font, 'Guess full keyword:', WHITE, (0, 3 * HEIGHT / 4 + TEXT_SIZE * 2))
                GUI.flip_cursor(WIN, input_size,
                                (len('Guess full keyword:') * AVG_TEXT_SIZE*1.2, 3 * HEIGHT / 4 + TEXT_SIZE * 3), cursorPos, flipCursor)
                GUI.draw_text_at(WIN, GUI.user_text, base_font,
                                 (len('Guess full keyword:') * AVG_TEXT_SIZE*1.2, 3 * HEIGHT / 4 + + TEXT_SIZE * 2))
