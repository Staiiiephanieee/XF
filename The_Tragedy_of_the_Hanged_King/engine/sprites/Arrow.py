#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pygame as pg
from .. import loader, observer


class Arrow(pg.sprite.Sprite):
    """
    Arrow to select restart or saved gamed.
    """

    def __init__(self, x, y):
        super(Arrow, self).__init__()
        self.image = loader.GFX['smallarrow']
        self.rect = self.image.get_rect(x=x, y=y)
        self.index = 0
        self.pos_list = [y, y + 34]
        self.allow_input = False
        self.pub = observer.Publisher()
        self.pub.register(observer.SoundEffects())

    def update(self):
        """
        update arrow position
        :return:
        """
        pass
