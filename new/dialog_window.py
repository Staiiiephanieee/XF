import sys
import pygame as pg
import os, sys, platform
import pickle, sys, os
import pygame as pg
from engine import tilerender
from engine.sprites import Player

class Dialog_window:
    def __init__(self, color, initial_position):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface([15, 15])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position
        self.going_down = True  # Start going downwards
        self.next_update_time = 0  # update() hasn't been called yet.还没有调用update


if __name__ == '__main__':
    Dialog_window()





    while not done:
        events = pg.event.get()

        for event in events:
            if event.type == pg.QUIT:
                done = True