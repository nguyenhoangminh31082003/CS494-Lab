import os
import enum

from pygame import image


# enum for screen view
class ScreenView(enum.IntEnum):
    REGISTER = 0
    WAIT = 1
    GAME = 2
    LOSE = 3
    STAT = 4

WIDTH, HEIGHT   = 1300, 600
ROW, COL        = 20, 20
LINE_SIZE       = 30
LINE_THICK      = 2
LINE_DISTANCE   = 6
MAX_NICKNAME    = 10
MAX_DOT         = 3
TEXT_SIZE       = 30
AVG_TEXT_SIZE   = 12
FPS             = 60
SCREEN_RATIO    = 0.5

BLANK_WORD              = '!@~'
PAUSE_TEXT              = 'Waiting for other players...'
END_TEXT                = 'END GAME'
ENTER_NICKNAME          = 'Enter your nickname:'
ERROR_MESSAGE_REGISTER  = 'Someone has already used this nickname'
INVALID_MESSAGE_REGISTER  = 'Invalid nickname'
TITLE                   = 'Magic Wheel'   
STATE_REGISTER              = 0
STATE_COMPLETE_REGISTER     = 1
STATE_PLAY_LETTER           = 2
STATE_PLAY_WORD             = 3
STATE_WAIT                  = 4
STATE_VIEW_RESULT           = 5
STATE_WAIT_WITHOUT_COUNT    = 6
STATE_END                   = 7

WHITE   = (255, 255, 255)
RED     = (150, 0, 0)
PAPER   = (240, 255, 240)
GREEN   = (0, 255, 0)
BLACK   = (0, 0, 0)
GRAY    = (252, 252, 252)
PINK    = (255, 192, 203)
AQUA    = (175, 238, 238)
GREEN   = (152, 251, 152)

IMAGE_PATH  = os.path.join(os.getcwd(), 'Assets')
BACKGROUND  = image.load(os.path.join(IMAGE_PATH, 'background.png'))
MENU        = image.load(os.path.join(IMAGE_PATH, 'menu.png'))
PLAY_BUTTON = image.load(os.path.join(IMAGE_PATH, 'playButton.png'))

AMATICSC_FONT       = os.path.join(IMAGE_PATH, 'Nunito.ttf')
VCR_OSD_MONO_FONT   = os.path.join(IMAGE_PATH, 'Nunito.ttf')