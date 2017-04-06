#!/usr/bin/env python
# -*- coding:utf-8 -*-

import random
import pygame as pg

from .. import constants as c

class CollisionHandler(object):

    def __init__(self, player, blockers, sprites):
        self.player = player
        self.static_blockers = blockers
        self.blockers = self.make_blocker_list(blockers, sprites)
        self.sprites = sprites

    def make_blocker_list(self, blockers, sprites):

        blocker_list = []

        for blocker in blockers:
            blocker_list.append(blocker)

        for sprite in sprites:
            blocker_list.extend(sprite.blockers)

        return blocker_list

    def update(self, current_time, keys ):
        self.blockers = self.make_blocker_list(self.static_blockers, self.sprites)
        self.player.rect.move_ip(self.player.x_vel, self.player.y_vel)
        self.check_for_blockers()

        if self.player.rect.x % 32 == 0 and self.player.rect.y % 32 == 0:
            if not self.player.state == 'resting':
                pass
            self.player.begin_resting()

    def check_for_blockers(self):
        player_collided = False

        for blocker in self.blockers:
            if self.player.rect.colliderect(blocker):
                player_collided = True
        if player_collided:
            self.reset_after_collision(self.player)
            self.player.begin_resting()

    def reset_after_collision(self, sprite):
        if sprite.x_vel != 0:
            sprite.rect.x -= sprite.x_vel
        else:
            sprite.rect.y -= sprite.y_vel