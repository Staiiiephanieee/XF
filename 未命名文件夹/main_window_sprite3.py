#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'wenfeng qiu'

"""This is a RPG game about a young , named wind."""

import sys
import pygame as pg
import os, sys, platform
from engine import tilerender
from engine.sprites import Player, Person
import random

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




if __name__ == '__main__':
    GAME = 'BEGIN GAME'

    GAME_CAPTION = 'XF game'

    os.environ['SDL_VIDEO_CENTERED'] = '1'
    if platform.system() == 'windows':
        os.chdir(os.path.dirname(sys.argv[0]))
    pg.init()
    pg.event.set_allowed([pg.KEYDOWN, pg.KEYUP, pg.QUIT])
    pg.display.set_caption(GAME_CAPTION)
    SCREEN = pg.display.set_mode((800, 608))
    SCREEN_RECT = SCREEN.get_rect()
    FONTS = load_all_fonts(os.path.join('resources', 'fonts'))
    MUSIC = load_all_music(os.path.join('resources', 'music'))
    GFX = load_all_gfx(os.path.join('resources', 'graphics'))
    SFX = load_all_sfx(os.path.join('resources', 'sound'))
    TMX = load_all_tmx(os.path.join('resources', 'tmx'))
    FONT = pg.font.Font(FONTS['Fixedsys500c'], 20)
    screen = pg.display.get_surface()
    clock = pg.time.Clock()
    # some about fps
    fps = 60
    show_fps = False
    done = False
    state_dict = {}  # state machine
    # current game state
    state_name = None
    state = None
    current_time = 0.0
    keys = pg.key.get_pressed()
    # music
    #set_music(MUSIC["kings_theme"], 0.4)
    # map
    tmx_map = TMX['background2']
    renderer = tilerender.Renderer(tmx_map)
    map_image = renderer.make_map()
    map_rect = map_image.get_rect()
    viewport = SCREEN.get_rect(bottom=map_rect.bottom)
    level_surface = pg.Surface(map_rect.size)
    level_rect = level_surface.get_rect()
    #title_box = GFX['title_box']
    #title_rect = title_box.get_rect()
    #title_rect.midbottom = viewport.midbottom
    #title_rect.y -= 30
    alpha = 255



    # player
    posx = 0
    posy = 0
    player = Player.Player('down')
    player.rect.x = posx
    player.rect.y = posy
    # blocks
    blockers = []
    for object in renderer.tmx_data.getObjects():
        #properties = object.__dict__
        #if properties['name'] == 'BLock':
        #    left = properties['x'] * 2
        #    top = (properties['y'] * 2) - 32;
        #    blocker = pg.Rect(left, top, 32, 32)
        #    blockers.append(blocker)
         if object.name == 'BLOCK':
             left = object.x-64
             top = object.y
             blocker = pg.Rect(left, top, 32, 32)
             blockers.append(blocker)
    for object in renderer.tmx_data.getObjects():
        properties = object.__dict__
        if object.name == 'spoint':

            posx = object.x+32
            posy = object.y
            print posx, posy
            player = Player.Player('down',posx, posy)
            player.rect.x = posx
            player.rect.y = posy
            break
        else:
            posx = 0
            posy = 0
            player = Player.Player('down')
            player.rect.x = posx
            player.rect.y = posy

	#****************************************************************************
    npc = Person.Person('player', 64, 128) # sprite
    #******************************************************************************

    # textbox
    #*****************************************************************************
    bground = GFX['dialoguebox']
    bgroundrect = bground.get_rect(centerx=400)

    bgroundimage = pg.Surface(bgroundrect.size)
    bgroundimage.set_colorkey((0,0,0))
    bgroundimage.blit(bground, (0, 0))
	
    #********************************************************************************

    while not done:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                done = True
            elif event.type == pg.KEYDOWN:
                keys = pg.key.get_pressed()
                if event.key == pg.K_F5:
                    show_fps = not show_fps
                    if not show_fps:
                        pg.display.set_caption(GAME_CAPTION)
            elif event.type == pg.KEYUP:
                keys = pg.key.get_pressed()
        current_time = pg.time.get_ticks()
        keys = pg.key.get_pressed()
        player.current_time = current_time
        player.keys = keys
        player.check_for_input()
        state_function = player.state_dict[player.state]
        state_function()
        player.rect.move_ip(player.x_vel, player.y_vel)
        player_collided=False
        #print (player.rect.x, player.rect.y)
        for blocker in blockers:
            if player.rect.colliderect(blocker):
                player_collided = True
        if player_collided:
            if player.x_vel != 0:
                player.rect.x -= player.x_vel
            else:
                player.rect.y -= player.y_vel
            player.begin_resting()



        if player.rect.x % 32 == 0 and player.rect.y % 32 == 0:
            if not player.state == 'resting':
                pass
            player.begin_resting()

        


        viewport.center = player.rect.center
        viewport.clamp_ip(level_rect)

     
        #**********************************************************************
        npc_collided=False
        if player.rect.colliderect(npc.rect):
        	npc_collided = True
        if npc_collided:
            if player.x_vel != 0:
                player.rect.x -= player.x_vel
            else:
                player.rect.y -= player.y_vel
            player.begin_resting()
        #***************************************************************************

       


        level_surface.blit(map_image, viewport, viewport)
        #level_surface.blit(title_box, title_rect)
        level_surface.blit(player.image, player.rect)
        level_surface.blit(npc.image, npc.rect)


		#*******************************************************************************
        if npc_collided:
        	#text = FONT.render('test', 1, (255, 0, 0))
        	#textpos = text.get_rect()
        	#textpos.x = viewport.x+300
        	#textpos.y = viewport.y+200
        	dialogue_image = FONT.render('hi, Stephanie',
                                          True,
                                          (255,0,0))
    		dialogue_rect = dialogue_image.get_rect(left=50, top=50)
    		bgroundimage.blit(dialogue_image, dialogue_rect)
    		bgroundrect.y = viewport.y+450
        	level_surface.blit(bgroundimage, bgroundrect)
 		#********************************************************************************************

        screen.blit(level_surface, (0, 0), viewport)
        pg.display.update()
        clock.tick(fps)

##        scripts_list = pg.sprite.Group()
##        scripts_list.add(script1)
##        scripts_list.add(script2)
##        sprites_hit_list = pg.sprite.spritecollide(player, scripts_list, True)
##        if len(sprites_hit_list) >0:
##            text = FONT.render('test', 1, (255, 0, 0))
##            textpos = text.get_rect()
##            textpos.x = box.x + 32
##            textpos.y = box.y + 32
        #yes = GFX['yes']
        #no = GFX['no']
        #yespos = yes.get_rect()
        #nopos = no.get_rect()
        #yespos.x = boxpos.x +32
        #yespos.y = boxpos.y +55
        #nopos.x = yespos.x + 64
        #nopos.y = yespos.y

       # rate = 60
       # frame = 25
       # last_time = 0
       # if current_time > last_time + rate:
       #     frame += 1
       #     if frame > last_time:
                #level_surface.blit(yes, yespos)
                #level_surface.blit(no, nopos)
        #        screen.blit(level_surface, (0, 0), viewport)
        #        pg.display.update()
        #        last_time = current_time
        #    framerate = pg.time.Clock()
        #    clock.tick(60)


        if show_fps:
            fps = clock.get_fps()
            with_fps = "{} - {:.2f} FPS".format(GAME_CAPTION, fps)
            pg.display.set_caption(with_fps)
    pg.quit()
    sys.exit()


