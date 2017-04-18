#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pygame as pg
from .. import loader, observer, core
import math, random
from itertools import izip

class Person(pg.sprite.Sprite):
    """
    Base class for all world characters controlled by the computer
    """
    def __init__(self, sheet_key, x, y, direction='down', state='resting', index=0):
        super(Person, self).__init__()
        self.alpha = 255
        self.name = sheet_key
        self.spritesheet_dict = self.create_spritesheet_dict(sheet_key)
        self.animation_dict = self.create_animation_dict()
        self.index = index
        self.direction = direction
        self.default_direction = direction
        self.image_list = self.animation_dict[self.direction]
        self.image = self.image_list[self.index]
        self.rect = self.image.get_rect(left=x, top=y)
        self.origin_pos = self.rect.topleft
        self.state_dict = self.create_state_dict()
        self.vector_dict = self.create_vector_dict()
        self.timer = 0.0
        self.current_time = 0.0
        self.move_timer = 0.0
        self.state = state
        self.blockers = self.set_blockers()
        self.location = self.get_tile_location()
        self.direction_list = ['up', 'down', 'left', 'right']
        self.x_vel = 0
        self.y_vel = 0
        self.pub = observer.Publisher()
        self.pub.register(observer.SoundEffects())


    def create_spritesheet_dict(self, sheet_key):
        """
        Make a dictionary of images from sprite sheet.
        :param sheet_key:
        :return:
        """
        image_list = []
        image_dict = {}
        sheet = loader.GFX[sheet_key]

        # image_keys = ['facing up 1', 'facing up 2', 'facing up 3', 'facing up 4',
        #               'facing down 1', 'facing down 2', 'facing down 3', 'facing down 4',
        #               'facing left 1', 'facing left 2', 'facing left 3', 'facing left 4',
        #               'facing right 1', 'facing right 2', 'facing right 3', 'facing right 4']

        image_keys = [
                      'facing down 1', 'facing down 2', 'facing down 3', 'facing down 4',
                      'facing left 1', 'facing left 2', 'facing left 3', 'facing left 4',
                      'facing right 1', 'facing right 2', 'facing right 3', 'facing right 4',
            'facing up 1', 'facing up 2', 'facing up 3', 'facing up 4']

        for row in range(2):
            for column in range(8):
                image_list.append(
                    core.extracts_image_from_sheet(column*32, row*32, 32, 32, sheet)
                )

        for key, image in izip(image_keys, image_list):
            image_dict[key] = image

        return image_dict

    def create_animation_dict(self):
        """
        Return a dictionary of image lists for animation.
        :return:
        """

        left_list = [ self.spritesheet_dict['facing left 1'], self.spritesheet_dict['facing left 2'],
                      self.spritesheet_dict['facing left 3'], self.spritesheet_dict['facing left 4']]
        right_list = [self.spritesheet_dict['facing right 1'], self.spritesheet_dict['facing right 2'],
                      self.spritesheet_dict['facing right 3'], self.spritesheet_dict['facing right 4']]
        up_list = [self.spritesheet_dict['facing up 1'], self.spritesheet_dict['facing up 2'],
                   self.spritesheet_dict['facing up 3'], self.spritesheet_dict['facing up 4']]
        down_list = [self.spritesheet_dict['facing down 1'], self.spritesheet_dict['facing down 2'],
                     self.spritesheet_dict['facing down 3'], self.spritesheet_dict['facing down 4']]

        direction_dict = {
            'left': left_list,
            'right': right_list,
            'up': up_list,
            'down': down_list
        }
        return direction_dict

    def create_state_dict(self):
        """
        Return a dictionary of all state methods.
        :return:
        """
        state_dict = {
            'resting': self.resting,
            'moving': self.moving,
            'animated resting': self.animated_resting,
            'autoresting': self.auto_resting,
            'automoving': self.auto_moving
        }
        return state_dict

    def create_vector_dict(self):
        """
        Return a dictionary of x and y velocities set to
        direction keys.
        :return:
        """
        vector_dict = {
            'up': (0, -1),
            'down': (0, 1),
            'left': (-1, 0),
            'right': (1, 0)
        }
        return vector_dict

    def update(self, current_time, *args):
        """
        Update sprite
        :param current_time:
        :param args:
        :return:
        """
        self.blockers = self.set_blockers()
        self.current_time = current_time
        self.image_list = self.animation_dict[self.direction]
        state_function = self.state_dict[self.state]
        state_function()
        self.location = self.get_tile_location()

    def set_blockers(self):
        """
        Sets blockers to prevent collision with other sprites.
        :return:
        """
        blockers = []

        if self.state == 'resting' or self.state == 'autoresting':
            blockers.append(pg.Rect(self.rect.x, self.rect.y, 32, 32))

        elif self.state == 'moving' or self.state == 'automoving':
            if self.rect.x % 32 == 0:
                tile_float = self.rect.y / float(32)
                tile1 = (self.rect.x, math.ceil(tile_float)*32)
                tile2 = (self.rect.x, math.floor(tile_float)*32)
                tile_rect1 = pg.Rect(tile1[0], tile1[1], 32, 32)
                tile_rect2 = pg.Rect(tile2[0], tile2[1], 32, 32)
                blockers.extend([tile_rect1, tile_rect2])

            elif self.rect.y % 32 == 0:
                tile_float = self.rect.x / float(32)
                tile1 = ( math.ceil(tile_float) * 32, self.rect.y )
                tile2 = ( math.floor(tile_float) * 32, self.rect.y )
                tile_rect1 = pg.Rect(tile1[0], tile1[1], 32, 32)
                tile_rect2 = pg.Rect(tile2[0], tile2[1], 32, 32)
                blockers.extend([tile_rect1, tile_rect2])
        return blockers

    def animation(self, freq=100):
        """
        Adjust sprite image frame based on timer
        :param freq:
        :return:
        """
        if (self.current_time - self.timer) > freq:
            #if self.index < (len(self.image_list) - 1):
            #    self.index += 1
            #else:
            #    self.index = 0
            self.index = (self.index+1) % len(self.image_list)
            self.timer = self.current_time
        self.image = self.image_list[self.index]

    def get_tile_location(self):
        """
        convert pygame coordinates into tile coordinates.
        :return:
        """
        if self.rect.x == 0:
            tile_x = 0
        elif self.rect.x % 32 == 0:
            tile_x = (self.rect.x / 32)
        else:
            tile_x = 0

        if self.rect.y == 0:
            tile_y = 0
        elif self.rect.y % 32 == 0:
            tile_y = (self.rect.y / 32)
        else:
            tile_y = 0
        return [tile_x, tile_y]

    def correct_position(self, rect_pos):
        """
        Adjust sprite position to be centered on tile.
        :param rect_pos:
        :return:
        """
        diff = rect_pos % 32
        if diff <= 16:
            return rect_pos - diff
        else:
            return rect_pos + diff

    def resting(self):
        """
        when the Person is not moving between tiles.
        Check if the player is centered on a tile.
        :return:
        """
        self.image = self.image_list[self.index]

        if self.rect.y % 32 != 0:
            self.rect.y = self.correct_position(self.rect.y)
        if self.rect.x % 32 != 0:
            self.rect.x = self.correct_position(self.rect.x)

    def moving(self):
        """
        Increment index and set self.image for animation.
        :return:
        """
        self.animation()
        assert ( self.rect.x % 32 == 0 or self.rect.y % 32 == 0), \
            'Not centered on tile'

    def animated_resting(self):
        self.animation(500)

    def auto_moving(self):
        """
        Animate sprite and check to stop.
        :return:
        """
        self.animation()
        assert (self.rect.x % 32 == 0 or self.rect.y % 32 == 0), \
            'Not centered on tile'

    def auto_resting(self):
        """
        Determine when to move a sprite from resting to moving in a random
        direction.
        :return:
        """
        self.image_list = self.animation_dict[self.direction]
        self.image = self.image_list[self.index]
        if self.rect.y % 32 != 0:
            self.rect.y = self.correct_position(self.rect.y)
        if self.rect.x % 32 != 0:
            self.rect.x = self.correct_position(self.rect.x)

        if (self.current_time - self.move_timer) > 2000:
            random_direction_list = self.direction_list
            random.shuffle(random_direction_list)
            direction = random_direction_list[0]
            self.begin_auto_moving(direction)
            self.move_timer = self.current_time

    def begin_moving(self, direction):
        """
        Transition the Person into the 'moving' state
        :param direction:
        :return:
        """
        self.direction = direction
        self.image_list = self.animation_dict[direction]
        self.timer = self.current_time
        self.move_timer = self.current_time
        self.state = 'moving'

        if self.rect.x % 32 == 0:
            self.y_vel = self.vector_dict[self.direction][1]
        if self.rect.y % 32 == 0:
            self.x_vel = self.vector_dict[self.direction][0]

    def begin_resting(self):
        """
        Transition the player into the 'resting' state
        :return:
        """
        self.state = 'resting'
        self.index = 1
        self.x_vel = self.y_vel = 0

    def begin_auto_moving(self, direction):
        """
        Transition sprite to a automatic moving state.
        :param direction:
        :return:
        """
        self.direction = direction
        self.image_list = self.animation_dict[direction]
        self.move_timer = self.current_time
        self.state = 'automoving'
        self.y_vel = self.vector_dict[self.direction][1]
        self.x_vel = self.vector_dict[self.direction][0]

    def beigin_auto_resting(self):
        """
        Transition sprite to an automatic resting state.
        :return:
        """
        self.state = 'autoresting'
        self.index = 1
        self.x_vel = self.y_vel = 0
        self.move_timer = self.current_time