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
        self.script1 = Scripts('script1', 32 * 7, 32 * 9.5)
        self.script2 = Scripts('script2', 32 * 13, 32 * 15.6)
        self.script3 = Scripts('script1', 32 * 2, 32 * 12.5)
        self.script4 = Scripts('script2', 32 * 3.5, 32 * 6)

        self.scripts_list.add(self.script1)
        self.scripts_list.add(self.script2)
        self.scripts_list.add(self.script3)
        self.scripts_list.add(self.script4)

        self.collide_scripts = False # scripts collide
        self.script_index = 0

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
        self.messagebox = MessageBox()

        #blocks
        self.blockers = []
        for object in self.renderer.tmx_data.getObjects():
            if object.name == 'BLOCK':
                left = object.x - 64
                top = object.y
                blocker = pg.Rect(left, top, 32, 32)
                self.blockers.append(blocker)

        #player
        self.boy1 = self.GFX['boy1']
        self.girl1 = self.GFX['girl1']

        self.player_index = 1

        self.boy1pos = self.boy1.get_rect()
        self.boy1pos.x = 100
        self.boy1pos.y = 125
        self.girl1pos = self.girl1.get_rect()
        self.girl1pos.x = 550
        self.girl1pos.y = 125

        self.player = None

        if self.player_index == 1:
            self.player = Player.Player('boy32', 'down')
            self.player.rect.x = 320
            self.player.rect.y = 320
            print 'boy'

        #texts on the first page
        self.atexts = AnimateText([
            {"text": "Hey dude, I need your help. Really, you need to listen to me.",
             "x": 32 * 0,
             "y": 32 * 2,
             "type": "text"},

            {"text": "I\'ve called the police but they didn\'t believe me.",
             "x": 32 * 0,
             "y": 32 * 3,
             "type": "text"},

            {"text": "What happened?",
             "x": 32 * 8,
             "y": 32 * 4,
             "type": "text"},

            {"text": "Okay ... I fainted,this is the last thing I\'ve remember.",
             "x": 32 * 0,
             "y": 32 * 5,
             "type": "text"},

            {"text": "But now,I\'m in a... I think this is an auditorium. And I\'m wearing a strange orange suit.",
             "x": 32 * 0,
             "y": 32 * 6,
             "type": "text"},

            {"text": "I was playing my phone somewhere I think and then...I just arrived here! Sounds crazy right?",
             "x": 32 * 0,
             "y": 32 * 7,
             "type": "text"},

            {"text": "It is indeed quite crazy  OR I believe you, dude.",
             "x": 32 * 8,
             "y": 32 * 8,
             "type": "button",
             "offset": 1},

            {"text": "Fine,anyway. I\'m trying to figure out how to get out of this place.Any suggestion?",
             "x": 32 * 0,
             "y": 32 * 9,
             "type": "text"},

            {"text": "Try the door! OR What\'s your staus?",
             "x": 32 * 8,
             "y": 32 * 10,
             "type": "button",
             "offset": 2},

            {"text": "Let me try...hmm...it\'s locked.",
             "x": 32 * 0,
             "y": 32 * 11,
             "type": "text",
             "offset": 2},

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
             "type": "text"},

            {"text": "No,I'll just call the police to let them pick you up.",
             "x": 32 * 8,
             "y": 32 * 16,
             "type": "text"},

            {"text": "No,no,no don\'t! I...no need for the cops,alright ?",
             "x": 32 * 0,
             "y": 32 * 17,
             "type": "text"},

            {"text": "Are you messing with the drugs again ?",
             "x": 32 * 8,
             "y": 32 * 18,
             "type": "text"},

            {"text": "No,I mean, a little, alright?",
             "x": 32 * 0,
             "y": 32 * 19,
             "type": "text"},

            {"text": "Seriously? Again? I mean, how long have you been out, 4 days ? ",
             "x": 32 * 8,
             "y": 32 * 20,
             "type": "text"},

            {"text": "Never again, okay? Go and find any address that could let me find where you are.",
             "x": 32 * 8,
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

            {"text": "I think this place is... \'Silver Central (Private)\'.",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Never heard of this strange name...Why there is a \"private\" in bracket?",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Hang on,I\'m working on the IP address.",
             "x": 32 * 8,
             "y": 32 * 24,
             "type": "text"},

            {"text": "[System entering]",
             "x": 32 * 8,
             "y": 32 * 24,
             "type": "text"},

            {"text": "[Access tampered]",
             "x": 32 * 8,
             "y": 32 * 24,
             "type": "text"},

            {"text": "[Visual signal stable]",
             "x": 32 * 8,
             "y": 32 * 24,
             "type": "text"},
        ])

        self.btexts = AnimateText([
            {"text": "PRESS \'9\' to enter the camera",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "button",
             "offset": 1},

            {"text": "Okay,I could see you.But the camera lost visual in long distance.",
             "x": 32 * 8,
             "y": 32 * 24,
             "type": "text"},

            {"text": "That\'s okay, it\'s not that dark here. Well, unless for that strange symbol.",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "You want me to take a photo so you could do some research on it?",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Sure",
             "x": 32 * 8,
             "y": 32 * 24,
             "type": "text"},

            {"text": "[Data received]",
             "x": 32 * 8,
             "y": 32 * 24,
             "type": "text"},

            {"text": "[Picture analyzing]",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Damn! It costs me 2% of the battery!",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Hang on, I\'m going to look up for a charger",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "[Scott is busy]",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "No.This place was nearly empty. Not even a rat!",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "I only found some wasted papers on the floor.",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Some of them seem to be torn up by a shredder.",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Want me to take a look at it?",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Yeah OR No,just leave it",
             "x": 32 * 8,
             "y": 32 * 24,
             "type": "button",
             "offset": 1},

            {"text": "Well,I think a glance will be fine, right ?",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "It\'s uh...",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "It\'s novel! I mean, a piece of a novel maybe.Why was it torn up?",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Could you find the title or read me a piece of the script?",
             "x": 32 * 8,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Okay, I didn\'t...",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Wait! A small line of words at the bottom of the paper!",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "\"The Hanged King's Tragedy\"?",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "What kind of stupid title was that?",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Jesus, man. I have to say that this place was really strange.",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Relax,I\'ll find out",
             "x": 32 * 8,
             "y": 32 * 24,
             "type": "text"},

            {"text": "[CAUTION >>> Picture analyze failed #:no data found]",
             "x": 32 * 8,
             "y": 32 * 24,
             "type": "text"},

            {
                "text": "The picture that you give me was just a logo of a holiday village. OR I didn\'t find anything about the picture.",
                "x": 32 * 3,
                "y": 32 * 24,
                "type": "button",
                "offset": 12},

            {"text": "That explains that stupid name.",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "But why would a holiday village lock me up here?",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "No,something must be wrong outside.",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Are you sure that nothing happened outside? Like a zombie outbreak or nuclear war?",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Nope.Just read the novel.",
             "x": 32 * 8,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Fine...",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {
                "text": "\'Petruccio and Gonzalo invite Sortino to dinner. They kill him and order the palace cooks to prepare the corpse as a stew.\'",
                "x": 32 * 0,
                "y": 32 * 24,
                "type": "text"},

            {"text": "\'Gonzalo orders Alinda, who witnessed the murder, to be locked up in the convent.\'",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Bloody and dirty, that\'s all that I could say",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Actually,I think this is more likely to be a summary of something instead of a novel.",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "This is the piece that I’ve got.",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {
                "text": "Then this place is the where the devil rests! I could feel it! The wicked gas that I\'m breathing.",
                "x": 32 * 0,
                "y": 32 * 24,
                "type": "text"},

            {"text": "Calm down. I\'m just joking.Haha.",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Okay, let\'s take a look at this strange novel",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {
                "text": "\'Petruccio and Gonzalo invite Sortino to dinner. They kill him and order the palace cooks to prepare the corpse as a stew.\'",
                "x": 32 * 0,
                "y": 32 * 24,
                "type": "text"},

            {"text": "\'Gonzalo orders Alinda, who witnessed the murder, to be locked up in the convent...\'",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "That\'s disgusting...really disgusting...",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "That\'s definitely written by a freak.",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Well, this is the only piece that I\'ve got.",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Well, I think you should find more of the summaries",
             "x": 32 * 8,
             "y": 32 * 24,
             "type": "text"},

            {"text": "You are right,but many of it was just strips that couldn\'t be read.",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Let\'s see...",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            # 游戏界面

            {"text": "Okay, it seems that I\'ve gathered a full piece of script here.There are some question marks.",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {
                "text": "No, I\'ll find out more about the place where you are. OR Send me the file and I\'ll take a look at it.",
                "x": 32 * 8,
                "y": 32 * 24,
                "type": "button",
                "offset": 2},

            {"text": "Well, I guess I\'ll just take a look at it.",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text",
             "offset": 5},

            {"text": "That's a good idea!",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Click \'send\'. Done!",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "[Incoming data]",
             "x": 32 * 8,
             "y": 32 * 24,
             "type": "text"},

            {"text": "[data downloading]",
             "x": 32 * 8,
             "y": 32 * 24,
             "type": "text"},

            # 玩家读剧本

            {"text": "Oh my god! I can\'t...Wow!",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "What happened?",
             "x": 32 * 8,
             "y": 32 * 24,
             "type": "text"},

            {"text": "People appeared on the stage! I mean, actors and actress!",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": " Go and ask for help!OR Hide yourself!",
             "x": 32 * 8,
             "y": 32 * 24,
             "type": "button",
             "offset": 7},

            {"text": "Hey guys!",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "I need help!",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "I was...",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "What the heck?",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Are they blind? They just...ignoring me.Like I was never here. Shout...",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Oh...shit...I hate to say dirty words but...",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text",
             "offset": 4},

            {"text": "Yes, I think I should hide.",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "This is too weird. How could they appear on the stage suddenly?",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "I mean, I\'ve checked the backstage before. It\'s empty.",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "You won\t believe this.",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "The symbol on their chest,it\'s the same as the one that is on the wall!",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Calm down,Scott",
             "x": 32 * 8,
             "y": 32 * 24,
             "type": "text"},

            {"text": "For hell I\'ll calm down! What is happening here?!!!!",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Deep breath,Scott.",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "D-CN-4050, could you hear me?",
             "x": 32 * 4,
             "y": 32 * 24,
             "type": "text"},

            {"text": "What?",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Who was that?",
             "x": 32 * 8,
             "y": 32 * 24,
             "type": "text"},

            {"text": "I don\'t know. Is it calling for me?",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "D-CN-4050, are you having contact with other D Class?",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "I suppose the answer should be \'no\'.",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "No,no. Absolutely no. Can you help me to get out of here?",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Preparing for experiment.",
             "x": 32 * 4,
             "y": 32 * 24,
             "type": "text"},

            {"text": "[SCP-701-EX-91]",
             "x": 32 * 4,
             "y": 32 * 24,
             "type": "text"},

            {"text": "[BEGIN]",
             "x": 32 * 4,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Wait,what?",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Okay, there\'s got to be someone outside who was imprisoning me.",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "But the actors are now acting the play.",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Are they psycopath?",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Hide! They might notice what you are doing! / Go on, tell me more about the situation",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "button",
             "offset": 4},

            {"text": "Yes...How stupid I am standing here!",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Wait, I\'ll check if there is more camera here.",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Into the corner...",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "Okay!",
             "offset": 14},

            {"text": "They are introducing themselves.",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Antonio? Isn\'t he...",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Damn! They are going to act that play!",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "[Warning. D class is contacting unauthorized personnel]",
             "x": 32 * 4,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Security, take him out.",
             "x": 32 * 4,
             "y": 32 * 24,
             "type": "text"},

            {"text": "No, you bastards! How could you",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "[GUNSHOT]",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Scott! Are you okay?",
             "x": 32 * 8,
             "y": 32 * 24,
             "type": "text",
             "offset": 98},

            {"text": "WARNING.Firewall disabled",
             "x": 32 * 8,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Incoming transmission >>>",
             "x": 32 * 8,
             "y": 32 * 24,
             "type": "text"},

            {"text": "This is SCP Foundation, unauthorized personnel,stay where you are and prepare to be arrested.",
             "x": 32 * 8,
             "y": 32 * 24,
             "type": "text"},

            {"text": "DO NOT ATTEMPT TO RESIST",
             "x": 32 * 8,
             "y": 32 * 24,
             "type": "text"},

            {"text": "DO NOT ATTEMPT TO RESIST",
             "x": 32 * 8,
             "y": 32 * 24,
             "type": "text",
             "offset": 93},

            {"text": "They are introducing themselves.",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Antonio? Isn\'t he...",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Damn! They are going to act that play!",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Why not watch the play?",
             "x": 32 * 8,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Man,you are definitely kidding right?",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "But the experiment!",
             "x": 32 * 8,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Yeah, that\'s strange...May be the experiment is about this drama thing!",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "But how boring they are! Testing a bloody drama play.",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "I\'ll watch it. I\'ll let you notice if anything goes wrong.",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Holy crap! What the fuck is that?",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Sorry for the language but...",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "That looks really creepy.",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "What happened?",
             "x": 32 * 8,
             "y": 32 * 24,
             "type": "text"},

            {"text": "It\'s uh...A guy who was covered in bandage and he was really scary.",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "The body was disproportionate. Long legs and skinny body.",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "And the actors aren\'t noticing this strange guy!",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "This is not good, really",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "D-CN-4050,report the current situation on the stage.",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Any benefit for me, Mr.Nobody?",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "D-CN-4050,report the current situation immediately or you\'ll be shot.This is warning shot.",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "[GUNSHOT]",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Oh, shit!",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "They\'ve got a gun!",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "I mean, an auto-gun turret on the wall!",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Where did that come from?",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Okay, Mr.Nobody,everything is going well.",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "The actors are acting normally about this play",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "D-CN-4050,What\'s the name of the King currently?",
             "x": 32 * 4,
             "y": 32 * 24,
             "type": "text"},

            {"text": "You will be replaced if you couldn't answer.",
             "x": 32 * 4,
             "y": 32 * 24,
             "type": "text"},

            {"text": "What the heck?",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Dude, you got to help me.",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Gonzalo OR Antonio",
             "x": 32 * 8,
             "y": 32 * 24,
             "type": "button",
             "offset": 2},

            {"text": "Thank you for your cooperation, D Class",
             "x": 32 * 4,
             "y": 32 * 24,
             "type": "text",
             "offset": 5},

            {"text": "Security, replace the D class.",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "What the...",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "[GUNSHOT]",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text",
             "offset": 57},

            {"text": "Scott! What happened?",
             "x": 32 * 8,
             "y": 32 * 24,
             "type": "text"},
            # Game over

            {"text": "D-CN-4050,Who was Petruccio ?",
             "x": 32 * 4,
             "y": 32 * 24,
             "type": "text"},

            {"text": "He was a noble lord allied with Gonzalo OR He was Antonio\'s best friend",
             "x": 32 * 8,
             "y": 32 * 24,
             "type": "button",
             "offset": 2},

            {"text": "Thank you for your answer, D-CN-4050",
             "x": 32 * 4,
             "y": 32 * 24,
             "type": "text",
             "offset": 6},

            {"text": "Security, replace the D class.",
             "x": 32 * 4,
             "y": 32 * 24,
             "type": "text"},

            {"text": "What the...",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "[GUNSHOT]",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text",
             "offest": 51},
            # Game over

            {"text": "D-CN-4050,is there any abnormal phenomena on stage?",
             "x": 32 * 4,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Yes...I suppose. Wait! The strange guy with bandage thing!",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Does that count?",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Ignore it.",
             "x": 32 * 4,
             "y": 32 * 24,
             "type": "text"},

            {"text": "D-CN-4050, Which ACT are you currently watching?",
             "x": 32 * 4,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Oh, Francisco is introducing this young lady Alinda to Antonio.",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Which act was it?",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "ACT 4 OR ACT 5",
             "x": 32 * 8,
             "y": 32 * 24,
             "type": "button",
             "offset": 2},

            {"text": "Thank you for your cooperation, D Class",
             "x": 32 * 4,
             "y": 32 * 24,
             "type": "text",
             "offset": 6},

            {"text": "Security, replace him.",
             "x": 32 * 4,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Go find another one",
             "x": 32 * 4,
             "y": 32 * 24,
             "type": "text"},

            {"text": "What the...",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "[GUNSHOT]",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text",
             "offset": 38},

            {"text": "Are you witnessing any violent behavior among the actors?",
             "x": 32 * 4,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Nope.",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Wait, what?",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "\"With this, fool\'s blood, it is the Hanged King\'s.\"",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Did you hear it?",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Perhaps that's actor's lines",
             "x": 32 * 8,
             "y": 32 * 24,
             "type": "text"},

            {"text": "No, I didn\'t see anything about it in the summary",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Oh! Jesus! Oh this is really...",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "[Barfing]",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "D-CN-4050 report what\'s happening.",
             "x": 32 * 4,
             "y": 32 * 24,
             "type": "text"},

            {"text": "You fucking bastards outside! Why don\'t you stop...Alinda is cutting Antonio\'s throat!",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "With that bloody long dagger!",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "And the fucking bandage guy was helping him!",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Stop it! For god sake!",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "I have to stop them, really. They are a bunch of crazy man.",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Hurry and help them! OR No, Stand down!",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "button",
             "offset": 1},

            {"text": "Fuck, why are they staring at me?",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "NO...THIS IS BAD...",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "\"With this, our blood, it is the Hanged King\'s.\"",
             "x": 32 * 4,
             "y": 32 * 24,
             "type": "text"},

            {"text": "This a damn revenge story! Completely off the script!",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "SCP-701 Containment breach.",
             "x": 32 * 4,
             "y": 32 * 24,
             "type": "text"},

            {"text": "I repeat, SCP-701 Containment breach",
             "x": 32 * 4,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Task Force, break in.",
             "x": 32 * 4,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Fuck it.Task Force is definitely not Santa Claus.",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Rush to the door! OR Run away from them!",
             "x": 32 * 8,
             "y": 32 * 24,
             "type": "button",
             "offset": 7},

            {"text": "Yes, rush to the door.",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "I might get out when they enters.",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Hang on, I might got...",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "[BREAK SOUND]",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Ahhhh...",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "************[SIGNAL LOST]************",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Thanks,dude. But I might not come through this.They are rushing towards me.",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Really fast.",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "And this is a small auditorium.",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Good to have...",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},

            {"text": "[BREAK SOUND]",
             "x": 32 * 4,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Task Force, this is containment command.",
             "x": 32 * 4,
             "y": 32 * 24,
             "type": "text"},

            {"text": "Fire at will.",
             "x": 32 * 4,
             "y": 32 * 24,
             "type": "text"},

            {"text": "************[SIGNAL LOST]************",
             "x": 32 * 0,
             "y": 32 * 24,
             "type": "text"},
        ])




class Scripts(pg.sprite.Sprite):
    def __init__(self, imagepath, x, y, scriptspath):
        pg.sprite.Sprite.__init__(self)
        self.image = load_all_gfx(os.path.join('resources', 'graphics'))[imagepath]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.iscollided = False
        self.isShow = True
        self.isTxtShow = False
        self.message = []
        pos = 0
        self.scriptspath = scriptspath

class MessageBox:
    def __init__(self):
        self.message_surface = pg.Surface((340, 356))
        self.render_size = 0
        self.message_surface_rect = self.message_surface.get_rect()
        self.message_surface_rect.x = 1000-350
        self.message_surface_rect.y = 600-200
        self.render_buff = []
        self.render_begin = 0
        self.isvalid = False
        self.isShow = True
        self.help_buf = [" help shdjsdhff83yhfjsd"]
        self.showhelp = False

    def update(self, image):
        if not self.showhelp:
            if not self.isvalid:
                self.message_surface = pg.Surface((340, 356))
                image = render_data.script1.scriptspath
                image.rect = image.get_rect()
                image.rect.x = 20
                image.rect.y = 32
                self.message_surface.blit(image, image.rect)

                self.isvalid = True
        box_rect = render_data.messagebox.message_surface_rect
        box_rect.x = render_data.boxpos.x+5
        box_rect.y = render_data.boxpos.y+5
        if self.isShow:
            render_data.level_surface.blit(render_data.messagebox.message_surface,box_rect)

    # def append_messages(self, messages):
    #     for i in range(0, len(messages)):
    #         self.render_buff.append(messages[i])
    #         self.render_size = self.render_size+1
    #         if self.render_size>10:
    #             self.render_begin = self.render_begin+1
    #     self.isvalid = False


    def check_for_input(self):
        for event in render_data.events:
            if event.type == pg.KEYDOWN:
                keys = pg.key.get_pressed()
                if event.key == pg.K_UP:
                    self.page_up()
                elif event.key == pg.K_DOWN:
                    self.page_down()
                elif event.key == pg.K_h:
                    self.toggle()

    def page_down(self):
        # self.message_surface.scroll(0, -32)
        if self.render_begin<self.render_size:
            self.render_begin=self.render_begin+1
            self.isvalid = False
        else:
            self.render_begin = self.render_size

    def page_up(self):
        # self.message_surface.scroll(0, 32)
        if self.render_begin>0:
            self.render_begin=self.render_begin-1
            self.isvalid = False
        else:
            self.render_begin = 0

    def toggle(self):
        self.isShow = not self.isShow



class AnimateText:
    def __init__(self, scripts):
        self.message_surface = pg.Surface((1000, 600))
        self.render_size = 0
        self.message_surface_rect = self.message_surface.get_rect()
        self.message_surface_rect.x = 0
        self.message_surface_rect.y = 0
        self.render_buff = []
        self.render_begin = 0
        self.isvalid = False
        self.isShow = True
        self.scripts = scripts
        self.scripts_index = 0
        self.scripts_pause = False
        self.current_time = pg.time.get_ticks()

    def update(self):
        time = pg.time.get_ticks()
        if (time - self.current_time) > 1000:
            self.append_script()
            self.current_time = time
        if not self.isvalid:
            self.message_surface = render_data.level_surface.copy()
            self.message_surface.fill((0, 0, 0))
            for i in range(0, 17):
                if (self.render_begin+i)<self.render_size:
                    text = render_data.FONT.render(self.render_buff[self.render_begin+i], 1, (255, 0, 0))
                    textpos = text.get_rect()
                    textpos.x = 20
                    textpos.y = 32 * (i) + 10
                    self.message_surface.blit(text, textpos)
                else:
                    break
            self.isvalid = True
            if self.isShow:
                messagebox_rect = self.message_surface.get_rect()
                render_data.level_surface.blit(self.message_surface, messagebox_rect)

    def append_script(self):
        if not self.scripts_pause:
            if self.scripts_index<len(self.scripts):
                if self.scripts[self.scripts_index]["type"]=='text':
                    self.append_message(self.scripts[self.scripts_index]["text"])
                    offset = 1
                    if self.scripts[self.scripts_index].has_key('offset'):
                        offset = self.scripts[self.scripts_index]["offset"]
                    self.scripts_index=self.scripts_index+offset
                elif self.scripts[self.scripts_index]["type"]=='button':
                    self.append_message(self.scripts[self.scripts_index]["text"])
                    self.scripts_pause = True

    def append_message(self, messages):
        self.render_buff.append(messages)
        self.render_size = self.render_size+1
        if self.render_size>17:
            self.render_begin = self.render_begin+1
        self.isvalid = False


    def check_for_input(self):
        for event in render_data.events:
            if event.type == pg.KEYDOWN:
                keys = pg.key.get_pressed()
                if event.key == pg.K_UP:
                    self.page_up()
                elif event.key == pg.K_DOWN:
                    self.page_down()
                elif event.key == pg.K_LEFT:
                    self.scripts_index = self.scripts_index+1
                    self.scripts_pause = False
                elif event.key == pg.K_RIGHT:
                    self.scripts_index = self.scripts_index + self.scripts[self.scripts_index]["offset"]
                    self.scripts_pause = False
                elif event.key == pg.K_h:
                    self.toggle()

    def page_down(self):
        # self.message_surface.scroll(0, -32)
        if self.render_begin<self.render_size:
            self.render_begin=self.render_begin+1
            self.isvalid = False
        else:
            self.render_begin = self.render_size

    def page_up(self):
        # self.message_surface.scroll(0, 32)
        if self.render_begin>0:
            self.render_begin=self.render_begin-1
            self.isvalid = False
        else:
            self.render_begin = 0

    def toggle(self):
        self.isShow = not self.isShow

def choose_player(render_data):
    pg.init()
    mouse_x, mouse_y = 0, 0

    while True:
    # if render_data.player_index == 0:
        for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()

                elif event.type == pg.MOUSEBUTTONDOWN:
                    pressed_array = pg.mouse.get_pressed()
                    for index in range(len(pressed_array)):
                        if pressed_array[index]:
                            if index==0 and 100 < mouse_x < 450 and 125 < mouse_y < 475:
                                print mouse_x, mouse_y
                                render_data.player_index = 1
                                print (render_data.player_index)
                                return ('START', render_data)

                            elif index==0 and 550 < mouse_x < 900 and 125 < mouse_y < 475:
                                render_data.player_index = 2
                                print render_data.player_index
                                render_data.player = Player.Player('girl32', 'down')
                                render_data.player.rect.x = 320
                                render_data.player.rect.y = 320
                                print 'boy'

                                return ('START', render_data)

                elif event.type == pg.MOUSEMOTION:
                    pos = pg.mouse.get_pos()
                    mouse_x = pos[0]
                    mouse_y = pos[1]
                    print mouse_x, mouse_y

        render_data.level_surface.blit(render_data.boy1, render_data.boy1pos)
        render_data.level_surface.blit(render_data.girl1, render_data.girl1pos)
        render_data.screen.blit(render_data.level_surface, (0, 0))
        pg.display.update()

    return ('CHOOSEPLAYER', render_data)


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
    # if atexts.scripts[atexts.scripts_index]["type"]=='button':
    render_data.atexts.check_for_input()
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

    # collide with the scripts
    sprites_collide_scripts = pg.sprite.spritecollide(render_data.player, render_data.scripts_list, True)
    for s in sprites_collide_scripts:
        s.iscollided = True
        s.isShow = False
        s.isTxtShow = True
        render_data.collide_scripts = True
        # script_index +=1

    # collide with the blockers
    for blocker in render_data.blockers:
        if render_data.player.rect.colliderect(blocker):
            player_collided_blocker = True
    if player_collided_blocker:
        if render_data.player.x_vel != 0:
            render_data.player.rect.x -= render_data.player.x_vel
        else:
            render_data.player.rect.y -= render_data.player.y_vel
            render_data.player.begin_resting()
        render_data.level_surface = pg.Surface(render_data.map_rect.size)
        render_data.atexts.index = 0
        if render_data.script_index == 4:
            return ("BLACKEND", render_data)

    if render_data.player.rect.x % 32 == 0 and render_data.player.rect.y % 32 == 0:
        if not render_data.player.state == 'resting':
            pass
            render_data.player.begin_resting()



    render_data.viewport.center = render_data.player.rect.center
    # render_data.viewport.center = (320, 330)
    render_data.viewport.clamp_ip(render_data.level_rect)
    render_data.level_surface.blit(render_data.map_image, render_data.viewport, render_data.viewport)

    # render box
    render_data.boxpos.x = render_data.viewport.x + (995 - render_data.boxpos.width)
    render_data.boxpos.y = render_data.viewport.y + (595 - render_data.boxpos.height)
    render_data.level_surface.blit(render_data.box, render_data.boxpos)

    # render scripts & message box
    if render_data.script1.isShow:
        render_data.level_surface.blit(render_data.script1.image, render_data.script1.rect)
    if render_data.script1.isTxtShow:
        render_data.messagebox.update()
        render_data.script1.isTxtShow = False
        render_data.script_index += 1

    if  render_data.script2.isShow:
        render_data.level_surface.blit(render_data.script2.image, render_data.script2.rect)
    if render_data.script2.isTxtShow:
        render_data.messagebox.update()
        render_data.script2.isTxtShow = False
        render_data.script_index += 1

    if render_data.script3.isShow:
        render_data.level_surface.blit(render_data.script3.image, render_data.script3.rect)
    if render_data.script3.isTxtShow:
        render_data.messagebox.update()
        render_data.script3.isTxtShow = False
        render_data.script_index += 1

    if  render_data.script4.isShow:
        render_data.level_surface.blit(render_data.script4.image, render_data.script4.rect)
    if render_data.script4.isTxtShow:
        render_data.messagebox.update()
        render_data.script4.isTxtShow = False
        render_data.script_index += 1

    # render player
    render_data.messagebox.update()
    render_data.messagebox.check_for_input()
    render_data.level_surface.blit(render_data.player.image, render_data.player.rect)


    #general
    render_data.screen.blit(render_data.level_surface, (0, 0), render_data.viewport)
    return ("LOADPLAYERMAP", render_data)

def black_end(render_data):
    for event in render_data.events:
        if event.type == pg.QUIT:
            done = True
        elif event.type == pg.KEYUP:
            keys = pg.key.get_pressed()

    render_data.btexts.update()
    render_data.screen.blit(render_data.level_surface, (0, 0))



    return ("BLACKEND", render_data)


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
    render_state_machine.add("CHOOSEPLAYER", choose_player)
    render_state_machine.add("START", start_game)
    render_state_machine.add("LOADPLAYERMAP", load_player_map)
    render_state_machine.add("BLACKEND",black_end)
    render_state_machine.add("GAMEOVER", None, end_state=1)
    render_state_machine.setStart("CHOOSEPLAYER")


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
