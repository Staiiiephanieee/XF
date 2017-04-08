#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pickle, sys, os
import pygame as pg
from .. import core, loader, tilerender, observer
from .. import constants as c
from engine.sprites.Arrow import *

if sys.version_info[0] == 2:
    import cPickle

    pickle = cPickle



class Menu(core._GameState):
    def __init__(self):
        super(Menu, self).__init__()
        self.music = loader.MUSIC['kings_theme']
        self.music_title = 'kings_theme'
        self.volume = 0.4
        self.next = c.INSTRUCTIONS
        self.tmx_map = loader.TMX['title']
        self.name = c.MAIN_MENU
        self.startup(0, 0)

    def startup(self, *args):
        self.renderer = tilerender.Renderer(self.tmx_map)
        self.map_image = self.renderer.make_2x_map()
        self.map_rect = self.map_image.get_rect()
        self.viewport = self.make_viewport(self.map_image)
        self.level_surface = pg.Surface(self.map_rect.size)
        self.title_box = self.set_image()
        self.title_rect = self.title_box.get_rect()
        self.title_rect.midbottom = self.viewport.midbottom
        self.title_rect.y -= 30
        self.state_dict = self.make_state_dict()
        self.state = c.TRANSITION_IN
        self.alpha = 255
        self.transition_surface = pg.Surface(loader.SCREEN_RECT.size)
        self.transition_surface.fill(c.BLACK_BLUE)
        self.transition_surface.set_alpha(self.alpha)
        self.game_data = core.create_game_data_dict()

    def make_state_dict(self):
        """
        Make the dictionary of state methods for the level.
        """
        state_dict = {c.TRANSITION_IN: self.transition_in,
                      c.TRANSITION_OUT: self.transition_out,
                      c.NORMAL: self.normal_update}

        return state_dict

    def update(self, surface, keys,  *args):
        update_level = self.state_dict[self.state]
        update_level(keys)
        self.draw_level()
        surface.blit(self.level_surface, (0, 0), self.viewport)
        surface.blit(self.transition_surface, (0, 0))

    def draw_level(self):
        """
        Blit tmx map and title box onto screen.
        """
        self.level_surface.blit(self.map_image, self.viewport, self.viewport)
        self.level_surface.blit(self.title_box, self.title_rect)


    def make_viewport(self, map_image):
        """
        Create the viewport to view the level through.
        """
        map_rect = map_image.get_rect()
        return loader.SCREEN.get_rect(bottomright=map_rect.bottomright)

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            self.state = c.TRANSITION_OUT

    def transition_in(self, *args):
        """
        Transition into scene with a fade.
        """
        self.transition_surface.set_alpha(self.alpha)
        self.alpha -= c.TRANSITION_SPEED
        if self.alpha <= 0:
            self.alpha = 0
            self.state = c.NORMAL

    def transition_out(self, *args):
        """
        Transition out of scene with a fade.
        """
        self.transition_surface.set_alpha(self.alpha)
        self.alpha += c.TRANSITION_SPEED
        if self.alpha >= 255:
            self.done = True

    def normal_update(self, *args):
        pass

    def set_image(self):
        """
        set title message box
        :return:
        """
        return loader.GFX['title_box']

class Instructions(Menu):
    """
    Instructions page.
    """
    def __init__(self):
        super(Instructions, self).__init__()
        self.music = None
        self.music_title = None
        self.next = c.LOADGAME


    def set_image(self):
        """
        set title message box
        :return:
        """
        return loader.GFX['instructions_box']

class LoadGame(Instructions):
    def __init__(self):
        super(LoadGame, self).__init__()
        self.pub = observer.Publisher()
        self.pub.register(observer.SoundEffects())
        self.allow_input = False
        self.arrow = Arrow(200, 260)
        self.arrow.pos_list[1] += 34

    def set_image(self):
        """
        set title message box
        :return:
        """
        return loader.GFX['loadgamebox']

    def draw_level(self):
        super(LoadGame, self).draw_level()
        self.level_surface.blit(self.arrow.image, self.arrow.rect)

    def get_event(self, event):
        pass # close the event

    def normal_update(self, keys):
        if self.allow_input:
            if keys[pg.K_DOWN] and self.arrow.index == 0:
                self.arrow.index = 1
                self.pub.dispatch(c.CLICK)
                self.allow_input = False
            elif keys[pg.K_UP] and self.arrow.index == 1:
                self.arrow.index = 0
                self.pub.dispatch(c.CLICK)
                self.allow_input = False
            elif keys[pg.K_SPACE]:
                self.next = c.OVERWORLD
                self.state = c.TRANSITION_OUT
                self.pub.dispatch(c.CLICK2)
            self.arrow.rect.y = self.arrow.pos_list[self.arrow.index]

        if not keys[pg.K_DOWN] and not keys[pg.K_UP]:
            self.allow_input = True



