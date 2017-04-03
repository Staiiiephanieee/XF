#!/usr/bin/env python
# -*- coding:utf-8 -*-

import copy, sys
import pygame as pg
from .. import loader, tilerender, core
from engine.sprites.Player import *
from engine.sprites.CollisionHandler import  *

class LevelState(core._GameState):

    def __init__(self, name):
        super(LevelState, self).__init__()
        self.name = name
        self.tmx_map = loader.TMX[name]
        self.music_title = None
        self.previous_music = None
        self.music = None
        self.volume = None

    def startup(self, current_time, game_data):
        self.game_data = game_data
        self.renderer = tilerender.Renderer(self.tmx_map)
        self.map_image = self.renderer.make_2x_map()
        self.map_rect = self.map_image.get_rect()
        self.viewport = self.make_viewport(self.map_image)
        self.level_surface = pg.Surface(self.map_rect.size)
        self.level_rect = self.level_surface.get_rect()
        self.player = self.make_player()
        self.blockers = self.make_blockers()
        self.sprites = self.make_sprites()
        self.collision_handler = CollisionHandler(self.player, self.blockers, self.sprites)

    def make_viewport(self, map_image):
        """
        Create the viewport to view the level through.
        """
        map_rect = map_image.get_rect()
        return loader.SCREEN.get_rect(bottom=map_rect.bottom)

    def make_player(self):
        for object in self.renderer.tmx_data.getObjects():
            properties = object.__dict__
            if properties['name'] == 'start point':
                posx = properties['x']*2
                posy = (properties['y']*2)-32
                player = Player(properties['direction'])
                player.rect.x = posx
                player.rect.y = posy
        return player

    def make_blockers(self):
        blockers = []

        for object in self.renderer.tmx_data.getObjects():
            properties = object.__dict__
            if properties['name'] == 'blocker':
                left = properties['x'] * 2
                top = ( properties['y'] * 2) - 32;
                blocker = pg.Rect(left, top, 32, 32)
                blockers.append(blocker)
        return blockers

    def make_sprites(self):
        sprites = pg.sprite.Group()
        return sprites

    def running_normally(self, surface, keys, current_time):
        self.player.update(current_time, keys)
        self.collision_handler.update(current_time, keys)
        self.viewport_update()
        self.draw_level(surface)

    def viewport_update(self):
        self.viewport.center = self.player.rect.center
        self.viewport.clamp_ip(self.level_rect)

    def draw_level(self, surface):
        self.level_surface.blit(self.map_image, self.viewport, self.viewport)
        self.level_surface.blit(self.player.image, self.player.rect)
        surface.blit(self.level_surface, (0,0), self.viewport)

    def update(self, surface, keys, current_time):
        self.running_normally(surface, keys, current_time)

    def update_game_data(self):
        self.game_data['last location'] = self.player.location
        self.game_data['last direction'] = self.player.direction
        self.game_data['last state'] = self.name
        self.set_new_start_pos()

    def set_new_start_pos(self):
        location = copy.deepcopy(self.game_data['last location'])
        direction = self.game_data['last direction']

        if direction == 'up':
            location[1] += 1
        elif direction == 'down':
            location[1] -= 1
        elif direction == 'left':
            location[0] += 1
        elif direction == 'right':
            location[0] -= 1
