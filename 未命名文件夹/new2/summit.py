#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'wenfeng qiu'

"""This is a RPG game about a young , named wind."""

import sys
import pygame as pg
from engine import loader
from engine.main import main

if __name__ == '__main__':
    loader.GAME
    main()
    pg.quit()
    sys.exit()
