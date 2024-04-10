import os

from pygame import image

ASSET_PATH  = os.path.join(os.getcwd(), 'Assets')

BACKGROUND  = image.load(os.path.join(ASSET_PATH, 'background.png'))
MENU        = image.load(os.path.join(ASSET_PATH, 'menu.png'))
PLAY_BUTTON = image.load(os.path.join(ASSET_PATH, 'playButton.png'))

AMATICSC_FONT       = os.path.join(ASSET_PATH, 'Nunito.ttf')
VCR_OSD_MONO_FONT   = os.path.join(ASSET_PATH, 'Nunito.ttf')