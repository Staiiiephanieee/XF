#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os, random
import pygame as pg
from . import constants as c

class EngineCore(object):
    """
    Engine Core for entie project. Sigle Object pattern. Contain the game loop,
    and contains the event_loop. Story follow a state machine.
    """

    def __init__(self, caption):
        self.screen = pg.display.get_surface()
        self.caption = caption
        self.clock = pg.time.Clock()
        # some about fps
        self.fps = 60
        self.show_fps = False
        self.done = False
        self.state_dict = {}  # state machine
        # current game state
        self.state_name = None
        self.state = None
        self.current_time = 0.0
        self.keys = pg.key.get_pressed()

    def startup(self, state_dict, start_state):  # set the state machie and start state
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]
        self.set_music()

    def flip_state(self):  # state machine transaction
        previous, self.state_name = self.state_name, self.state.next
        previous_music = self.state.music_title
        persist = self.state.cleanup()  # game data
        self.state = self.state_dict[self.state_name]
        self.state.previous = previous
        self.state.previous_music = previous_music
        self.state.startup(self.current_time, persist)
        self.set_music()

    def update(self):
        self.current_time = pg.time.get_ticks()
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(self.screen, self.keys, self.current_time)

    def set_music(self):
        """
        Set music for the new state
        """
        if self.state.music_title == self.state.previous_music:
            pass
        elif self.state.music:
            pg.mixer.music.load(self.state.music)
            pg.mixer.music.set_volume(self.state.volume)
            pg.mixer.music.play(-1)

    def event_loop(self):
        self.events = pg.event.get()

        for event in self.events:
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == pg.KEYDOWN:
                self.keys = pg.key.get_pressed()
                self.toggle_show_fps(event.key)  # check is toggle F5
                self.state.get_event(event)  # key event about current state
            elif event.type == pg.KEYUP:
                self.keys = pg.key.get_pressed()
                self.state.get_event(event)

    def toggle_show_fps(self, key):
        if key == pg.K_F5:
            self.show_fps = not self.show_fps
            if not self.show_fps:
                pg.display.set_caption(self.caption)

    def run(self):
        """Main loop for entire program"""
        while not self.done:
            self.event_loop()
            self.update()
            pg.display.update()
            self.clock.tick(self.fps)
            if self.show_fps:
                fps = self.clock.get_fps()
                with_fps = "{} - {:.2f} FPS".format(self.caption, fps)
                pg.display.set_caption(with_fps)


class _GameState(object):
    """ Base class for all game states"""

    def __init__(self):
        self.next = None
        self.previous = None
        self.game_data = {}
        self.music = None
        self.music_title = None
        self.previous_music = None
        self.done = False
        self.quit = False

    def get_event(self, event):
        pass

    def startup(self, game_data):
        self.game_data = game_data

    def cleanup(self):
        self.done = False
        return self.game_data

    def update(self, surface, keys, current_time):
        pass


def load_all_gfx(directory, colorkey=(255, 0, 255), accept=('.png', 'jpg', 'bmp')):
    graphics = {}
    for pic in os.listdir(directory):
        name, ext = os.path.splitext(pic)
        if ext.lower() in accept:
            img = pg.image.load(os.path.join(directory, pic))
            if img.get_alpha():
                img = img.convert_alpha()
            else:
                img = img.convert()
                img.set_colorkey(colorkey)
            graphics[name] = img
    return graphics


def load_all_resource_path(directory, accept=()):
    pathdict = {}
    for res in os.listdir(directory):
        name, ext = os.path.splitext(res)
        if ext.lower() in accept:
            pathdict[name] = os.path.join(directory, res)
    return pathdict


def load_all_music(directory, accept=('.wav', '.mp3', '.ogg', '.mdi')):
    return load_all_resource_path(directory, accept)


def load_all_fonts(directory, accept=('.ttf')):
    return load_all_resource_path(directory, accept)


def load_all_tmx(directory, accept=('.tmx')):
    return load_all_resource_path(directory, accept)


def load_all_sfx(directory, accept=('.wav', '.mp3', '.ogg', '.mdi')):
    effects = {}
    for fx in os.listdir(directory):
        name, ext = os.path.splitext(fx)
        if ext.lower() in accept:
            effects[name] = pg.mixer.Sound(os.path.join(directory, fx))
    return effects


def extracts_image_from_sheet(x, y, width, height, sprite_sheet):
    """
    Extracts image from sprite sheet
    :param x:
    :param y:
    :param width:
    :param height:
    :param sprite_sheet:
    :return:
    """
    image = pg.Surface([width, height])
    rect = image.get_rect()
    image.blit(sprite_sheet, (0, 0), (x, y, width, height))
    image.set_colorkey(c.BLACK)
    return image

def create_game_data_dict():
    """
    Create a dictionary of persistant values the player
    :return:
    """
    data_dict = {
        'last location': None,
        'last state': None,
        'last direction': None
    }
    return data_dict