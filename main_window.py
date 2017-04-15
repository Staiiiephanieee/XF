#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os, sys, platform
import pygame as pg
from util import *
from StateMachine import *
from engine.tilerender import *
from engine.sprites import Player, Person




class GameRenderData:
    def __init__(self):
        pg.init()
        self.GAME = 'BEGIN GAME'
        self.GAME_CAPTION = 'XF game'
        self.FONTS = load_all_fonts(os.path.join('resources', 'fonts'))
        self.MUSIC = load_all_music(os.path.join('resources', 'music'))
        self.GFX = load_all_gfx(os.path.join('resources', 'graphics'))
        self.SFX = load_all_sfx(os.path.join('resources', 'sound'))
        self.TMX = load_all_tmx(os.path.join('resources', 'tmx'))
        self.FONT = pg.font.Font(self.FONTS['Fixedsys500c'], 14)

        self.events = None
        self.viewport = None
        self.level_surface = None
        self.level_rect = None
        self.screen = pg.display.get_surface()

        # initialization dialog box
        self.bground = self.GFX['box']
        self.bgroundrect = self.bground.get_rect(centerx=400)
        self.bgroundimage = pg.Surface(self.bgroundrect.size)
        self.bgroundimage.set_colorkey((0, 0, 0))
        self.bgroundimage.blit(self.bground, (0, 0))

        # scripts
        self.scripts_list = pg.sprite.Group()
        self.script1 = Scripts('script1', 235, 32 * 9.5)
        self.script2 = Scripts('script2', 32 * 7, 32 * 15.6)

        self.scripts_list.add(self.script1)
        self.scripts_list.add(self.script2)
        # for i in range(2):
        #     script = Scripts("script%s"%(i+1), 64*i+635, 32*9.5+32*5*i)
        #     self.scripts_list.add(script)

        self.collide_scripts = False # scripts collide

        # map
        self.tmx_map = self.TMX['background2']
        self.renderer = Renderer(self.tmx_map)
        self.map_image = self.renderer.make_map()
        self.map_rect = self.map_image.get_rect()
        self.viewport = SCREEN.get_rect(bottom=self.map_rect.bottom)
        self.level_surface = pg.Surface(self.map_rect.size)
        self.level_rect = self.level_surface.get_rect()

        # box
        self.box = self.GFX["box"]
        self.boxpos = self.box.get_rect()
        print(self.viewport.x, self.viewport.y)

        #blocks
        self.blockers = []
        for object in self.renderer.tmx_data.getObjects():
            if object.name == 'BLOCK':
                left = object.x - 64
                top = object.y
                blocker = pg.Rect(left, top, 32, 32)
                self.blockers.append(blocker)

        #player
        self.player = None
        for object in self.renderer.tmx_data.getObjects():
            properties = object.__dict__
            if object.name == 'spoint':
                posx = object.x + 32
                posy = object.y
                self.player = Player.Player('girl32', 'down', posx, posy)
                self.player.rect.x = posx
                self.player.rect.y = posy
            else:
                self.player = Player.Player('girl32', 'down')
                self.player.rect.x = 320
                self.player.rect.y = 320

        #texts on the first page
        self.atexts = AnimateText([
            {"text": "Hey dude, I need your help. Really, you need to listen to me.",
             "x": 32 * 1,
             "y": 32 * 2,
             "type": "text"},
            {"text": "I\'ve called the police but they didn\'t believe me.",
             "x": 32 * 1,
             "y": 32 * 3,
             "type": "text"},

            {"text": "What happened?",
             "x": 32 * 8,
             "y": 32 * 4,
             "type": "text"},

            {"text": "Okay ... I fainted,this is the last thing I\'ve remember.",
             "x": 32 * 1,
             "y": 32 * 5,
             "type": "text"},

            {"text": "But now,I\'m in a... I think this is an auditorium. And I\'m wearing a strange orange suit.",
             "x": 32 * 1,
             "y": 32 * 6,
             "type": "text"},

            {"text": "I was playing my phone somewhere I think and then...I just arrived here! Sounds crazy right?",
             "x": 32 * 1,
             "y": 32 * 7,
             "type": "text"},

            {"text": "It is indeed quite crazy  OR I believe you, dude.",
             "x": 32 * 8,
             "y": 32 * 8,
             "type": "button_u"},

            {"text": "Fine,anyway. I\'m trying to figure out how to get out of this place.Any suggestion?",
             "x": 32 * 0,
             "y": 32 * 9,
             "type": "text"},

            {"text": "Try the door! OR What\'s your staus?",
             "x": 32 * 8,
             "y": 32 * 10,
             "type": "button"},

            {"text": "Let me try...hmm...it\'s locked.",
             "x": 32 * 0,
             "y": 32 * 11,
             "type": "text"},

            {"text": "I\'m fine! Luckily not being harmed. At least I have my kidney preserved.",
             "x": 32 * 0,
             "y": 32 * 12,
             "type": "text"},

            {"text": "My phone got...24% of the battery and that's the only thing that links us now.",
             "x": 32 * 0,
             "y": 32 * 13,
             "type": "text"},

            {"text": 'Hang on! There\'s a camera!I know you could hack into it,right?',
             "x": 32 * 0,
             "y": 32 * 14,
             "type": "text"},

            {"text": "I need the something to tell me where you are so I could get the IP address.",
             "x": 32 * 8,
             "y": 32 * 15,
             # "jump": 2,
             "type": "text"},

            {"text": "No,I'll just call the police to let them pick you up.",
             "x": 32 * 8,
             "y": 32 * 16,
             "type": "text"},

            {"text": "No,no,no don't! I...no need for the cops,alright?",
             "x": 32 * 0,
             "y": 32 * 17,
             "type": "text"},

            {"text": "Are you messing with the drugs again?",
             "x": 32 * 8,
             "y": 32 * 18,
             "type": "text"},

            {"text": "No,I mean, a little, alright?",
             "x": 32 * 0,
             "y": 32 * 19,
             "type": "text"},

            {"text": "Seriously? Again? I mean, how long have you been out, 4 days ? ",
             "x": 32 * 0,
             "y": 32 * 20,
             "type": "text"},

            {"text": "Never again, okay? Go and find any address that could let me find where you are.",
             "x": 32 * 0,
             "y": 32 * 21,
             "type": "text"},

            {"text": "Okay then, there\'s definitely something with a name tag here.",
             "x": 32 * 0,
             "y": 32 * 22,
             "type": "text"},

            {"text": "Wait...",
             "x": 32 * 0,
             "y": 32 * 23,
             "type": "text"},
            # 此处有假进度条
            {"text": "Okay...Here are some more.",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},
                ])

# class TEXT:
#     def __init__(self, text, x, y):
#         self.text = render_data.FONT.render(text, 1, (225, 0, 0))
#         self.textpos = self.text.get_rect()
#         self.textpos.x = x
#         self.textpos.y = y
#         render_data.level_surface.blit(self.text, self.textpos)
#         render_data.screen.blit(render_data.level_surface, (0, 0))
#         # pg.time.delay(2000)

class Scripts(pg.sprite.Sprite):
    def __init__(self, imagepath, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = load_all_gfx(os.path.join('resources', 'graphics'))[imagepath]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    # def update(self):
    #     print ("blit")
    #     pg.Surface(Renderer(load_all_tmx(os.path.join('resources', 'tmx'))["background2"]).make_map().get_rect().size).blit(self.image, self.rect)


class AnimateText:
    def __init__(self, texts):
        self.texts = texts
        self.index = 0
        self.current_time = pg.time.get_ticks()

    def update(self):
        # print (self.index)
        time = pg.time.get_ticks()
        if (self.index < len(self.texts)):
            if (time - self.current_time) > 1000:
                if self.texts[self.index]["type"]=="button":
                    self.text = render_data.FONT.render(self.texts[self.index]["text"], 1, (225, 0, 0))
                    self.textpos = self.text.get_rect()
                    self.textpos.x = self.texts[self.index]["x"]
                    self.textpos.y = self.texts[self.index]["y"]
                    render_data.level_surface.blit(self.text, self.textpos)
                    for event in render_data.events:
                        if event.type == pg.KEYDOWN:
                            keys = pg.key.get_pressed()
                            if event.key == pg.K_SPACE:
                                self.current_time = time
                                self.index = self.index + 1
                                self.current_time = time
                                print "Yes"
                                break
                            elif event.key == pg.K_RETURN:
                                self.current_time = time
                                self.index = self.index + 1
                                self.current_time = time
                                print "No"
                                break
                else:
                    self.text = render_data.FONT.render(self.texts[self.index]["text"], 1, (225, 0, 0))
                    self.textpos = self.text.get_rect()
                    self.textpos.x = self.texts[self.index]["x"]
                    self.textpos.y = self.texts[self.index]["y"]
                    render_data.level_surface.blit(self.text, self.textpos)
                    self.current_time = time
                    self.index = self.index + 1

    def Toggle(self):
        self.pause = not self.pause

def start_game(render_data):

    for event in render_data.events:
        if event.type == pg.QUIT:
            done = True
        elif event.type == pg.KEYDOWN:
            keys = pg.key.get_pressed()
            if event.key == pg.K_9:
                return ("LOADPLAYERMAP", render_data)
        elif event.type == pg.KEYUP:
            keys = pg.key.get_pressed()

    render_data.atexts.update()
    render_data.screen.blit(render_data.level_surface, (0, 0))



    return ("START", render_data)

def load_player_map(render_data):
    # initialization dialog box
    #palyer position
    current_time = pg.time.get_ticks()
    keys = pg.key.get_pressed()
    render_data.player.current_time = current_time
    render_data.player.keys = keys
    render_data.player.check_for_input()
    state_function = render_data.player.state_dict[render_data.player.state]
    state_function()
    render_data.player.rect.move_ip(render_data.player.x_vel, render_data.player.y_vel)
    player_collided_blocker = False

    for blocker in render_data.blockers:
        if render_data.player.rect.colliderect(blocker):
            player_collided_blocker = True
    if player_collided_blocker:
        if render_data.player.x_vel != 0:
            render_data.player.rect.x -= render_data.player.x_vel
        else:
            render_data.player.rect.y -= render_data.player.y_vel
            render_data.player.begin_resting()

    if render_data.player.rect.x % 32 == 0 and render_data.player.rect.y % 32 == 0:
        if not render_data.player.state == 'resting':
            pass
            render_data.player.begin_resting()

    # collide with the scripts
    sprites_collide_scripts = pg.sprite.spritecollide(render_data.player, render_data.scripts_list, True)
    if len(sprites_collide_scripts) >0:
        print 'collide scripts'
        render_data.collide_scripts = True

    render_data.viewport.center = render_data.player.rect.center
    # render_data.viewport.center = (320, 330)
    render_data.viewport.clamp_ip(render_data.level_rect)

    render_data.level_surface.blit(render_data.map_image, render_data.viewport, render_data.viewport)
    # render box
    # print (render_data.viewport.x, render_data.viewport.y)
    render_data.boxpos.x = render_data.viewport.x + (1200 - render_data.boxpos.width)
    render_data.boxpos.y = render_data.viewport.y + (600 - render_data.boxpos.height)
    render_data.level_surface.blit(render_data.box, render_data.boxpos)
    # render scripts
    render_data.level_surface.blit(render_data.script1.image, render_data.script1.rect)
    render_data.level_surface.blit(render_data.script2.image, render_data.script2.rect)
    # render player
    render_data.level_surface.blit(render_data.player.image, render_data.player.rect)

    if render_data.collide_scripts == True:
        text = render_data.FONT.render('test', 1, (255, 0, 0))
        textpos = text.get_rect()
        textpos.x = render_data.boxpos.x + 32
        textpos.y = render_data.boxpos.y + 32
        render_data.level_surface.blit(text, textpos)
        # render_data.collide_scripts = False

    render_data.screen.blit(render_data.level_surface, (0, 0), render_data.viewport)
    return ("LOADPLAYERMAP", render_data)


    # return ("LOADPLAYER", render_data)

if __name__ == "__main__":

    os.environ['SDL_VIDEO_CENTERED'] = '1'
    if platform.system() == 'windows':
        os.chdir(os.path.dirname(sys.argv[0]))
    pg.init() # pygame initialize

    pg.event.set_allowed([pg.KEYDOWN, pg.KEYUP, pg.QUIT])  # set we should focus event

    SCREEN = pg.display.set_mode((1000, 600)) # set screen size
    SCREEN_RECT = SCREEN.get_rect()

    # new a GameRenderData
    render_data = GameRenderData()
    pg.display.set_caption(render_data.GAME_CAPTION)  # set game caption

    clock = pg.time.Clock()

    # some about fps
    fps = 60
    show_fps = False
    done = False



    # new a render state machine
    render_state_machine = StateMachine()
    render_state_machine.add("START", start_game)
    render_state_machine.add("LOADPLAYERMAP", load_player_map)
    render_state_machine.add("GAMEOVER", None, end_state=1)
    render_state_machine.setStart("START")


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
                        pg.display.set_caption(render_data.GAME_CAPTION)
            elif event.type == pg.KEYUP:
                keys = pg.key.get_pressed()
        render_data.events = events
        render_state_machine.update(render_data)
        pg.display.update()
        clock.tick(fps)

        if show_fps:
            fps = clock.get_fps()
            with_fps = "{} - {:.2f} FPS".format(render_data.GAME_CAPTION, fps)
            pg.display.set_caption(with_fps)
    pg.quit()
    sys.exit()
