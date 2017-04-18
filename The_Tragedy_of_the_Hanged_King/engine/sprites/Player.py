#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pygame as pg
from .. import loader, observer, core
import math, random
from itertools import izip
from . import Person

class Player(Person.Person):
    """
    User controlled character
    """

    def __init__(self,playername, direction='down', x=0, y=0, state='resting', index=0):
        super(Player, self).__init__(playername, x, y, direction, state, index)
        self.index = 1
        self.image = self.image_list[self.index]

    def create_vector_dict(self):
        """
        Return a dictionary of x and y velocities set to
        direction keys.
        :return:
        """
        vector_dict = {
            'up': (0, -2),
            'down': (0, 2),
            'left': (-2, 0),
            'right': (2, 0)
        }
        return vector_dict

    def update(self, current_time, keys, *args):
        self.current_time = current_time
        self.keys = keys
        self.check_for_input()
        self.blockers = self.set_blockers()
        state_function = self.state_dict[self.state]
        state_function()
        self.location = self.get_tile_location()

    def check_for_input(self):
        """
        Checks for player input
        :return:
        """
        if self.state == 'resting':
            if self.keys[pg.K_w]:
                self.begin_moving('up')
            elif self.keys[pg.K_s]:
                self.begin_moving('down')
            elif self.keys[pg.K_a]:
                self.begin_moving('left')
            elif self.keys[pg.K_d]:
                self.begin_moving('right')
