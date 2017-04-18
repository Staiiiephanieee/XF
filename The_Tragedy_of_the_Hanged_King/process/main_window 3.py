#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os, sys, platform
import pygame as pg
from util import *
from StateMachine import *
from engine import tilerender

class GameRenderData:
    def __init__(self):
        self.GAME = 'BEGIN GAME'
        self.GAME_CAPTION = 'XF game'

        # load game's resources
        self.FONTS = load_all_fonts(os.path.join('resources', 'fonts'))
        self.MUSIC = load_all_music(os.path.join('resources', 'music'))
        self.GFX = load_all_gfx(os.path.join('resources', 'graphics'))
        self.SFX = load_all_sfx(os.path.join('resources', 'sound'))
        self.TMX = load_all_tmx(os.path.join('resources', 'tmx'))
        self.FONT = pg.font.Font(self.FONTS['Fixedsys500c'], 20)

        self.screen = pg.display.get_surface()
        self.events = None
        self.viewport = None
        self.level_surface = None
        self.level_rect = None


def start_game(render_data):
    # initialization dialog box
    bground = render_data.GFX['box']
    bgroundrect = bground.get_rect(centerx=400)

    bgroundimage = pg.Surface(bgroundrect.size)
    bgroundimage.set_colorkey((0, 0, 0))
    bgroundimage.blit(bground, (0, 0))


    for event in render_data.events:
        if event.type == pg.QUIT:
            done = True
        elif event.type == pg.KEYDOWN:
            keys = pg.key.get_pressed()
            if event.key == pg.K_SPACE:
                return ("LOADMAP", render_data)
        elif event.type == pg.KEYUP:
            keys = pg.key.get_pressed()
    # render welcome message
    dialogue_image = render_data.FONT.render('hi, Stephanie',
                                 True,
                                 (255, 0, 0))
    dialogue_rect = dialogue_image.get_rect(left=50, top=50)
    bgroundimage.blit(dialogue_image, dialogue_rect)
    bgroundrect.y = 450
    render_data.screen.blit(bgroundimage, bgroundrect)

    return ("START", render_data)

def load_map(render_data):
    # initialization map
    tmx_map = render_data.TMX['background2']
    renderer = tilerender.Renderer(tmx_map)
    map_image = renderer.make_map()
    map_rect = map_image.get_rect()
    render_data.viewport = SCREEN.get_rect(bottom=map_rect.bottom)
    render_data.level_surface = pg.Surface(map_rect.size)
    render_data.level_rect = render_data.level_surface.get_rect()

    render_data.viewport.center = (320,320)
    render_data.viewport.clamp_ip(render_data.level_rect)


    render_data.level_surface.blit(map_image, render_data.viewport, render_data.viewport)
    render_data.screen.blit(render_data.level_surface, (0, 0), render_data.viewport)

    return ("LOADMAP", render_data)

if __name__ == "__main__":

    os.environ['SDL_VIDEO_CENTERED'] = '1'
    if platform.system() == 'windows':
        os.chdir(os.path.dirname(sys.argv[0]))
    pg.init() # pygame initialize
    pg.event.set_allowed([pg.KEYDOWN, pg.KEYUP, pg.QUIT])  # set we should focus event
    SCREEN = pg.display.set_mode((800, 608)) # set screen size
    SCREEN_RECT = SCREEN.get_rect()
    render_data = GameRenderData()
    pg.display.set_caption(render_data.GAME_CAPTION)  # set game caption
    clock = pg.time.Clock()

    # some about fps
    fps = 60
    show_fps = False
    done = False

    # new a GameRenderData


    # new a render state machine
    render_state_machine = StateMachine()
    render_state_machine.add("START", start_game)
    render_state_machine.add("LOADMAP", load_map)
    render_state_machine.add("GAMEOVER", None, end_state=1)
    render_state_machine.setStart("START")


    while not done:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                done = True
            elif event.type == pg.KEYDOWN:
                keys = pg.key.get_pressed()
                if event.key == pg.K_F5:
                    show_fps = not show_fps
                    if not show_fps:
                        pg.display.set_caption(render_data.GAME_CAPTION)
            elif event.type == pg.KEYUP:
                keys = pg.key.get_pressed()
        render_data.events = events
        render_state_machine.update(render_data)
        pg.display.update()
        clock.tick(fps)

        if show_fps:
            fps = clock.get_fps()
            with_fps = "{} - {:.2f} FPS".format(render_data.GAME_CAPTION, fps)
            pg.display.set_caption(with_fps)
    pg.quit()
    sys.exit()
