#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os, sys, platform
import pygame as pg

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


def set_music(title, volume):
    pg.mixer.music.load(title)
    pg.mixer.music.set_volume(volume)
    pg.mixer.music.play(-1)
