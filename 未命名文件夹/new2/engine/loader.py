#-*- coding:utf-8 -*- 

"""
This module initializes the display and load resources.
"""

import os, sys, platform
import pygame as pg
from . import core


GAME = 'BEGIN GAME'

GAME_CAPTION = 'simple game'

os.environ['SDL_VIDEO_CENTERED'] = '1'
if platform.system()=='windows':
    os.chdir(os.path.dirname(sys.argv[0]))
pg.init()
pg.event.set_allowed([pg.KEYDOWN, pg.KEYUP, pg.QUIT])
pg.display.set_caption(GAME_CAPTION)
SCREEN = pg.display.set_mode((800, 608))
SCREEN_RECT = SCREEN.get_rect()

FONTS = core.load_all_fonts(os.path.join('resources', 'fonts'))
MUSIC = core.load_all_music(os.path.join('resources', 'music'))
GFX = core.load_all_gfx(os.path.join('resources', 'graphics'))
SFX = core.load_all_sfx(os.path.join('resources', 'sound'))
TMX = core.load_all_tmx(os.path.join('resources', 'tmx'))

FONT = pg.font.Font(FONTS['Fixedsys500c'], 20)