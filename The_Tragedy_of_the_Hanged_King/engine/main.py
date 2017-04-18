#!/usr/bin/env python
# -*- coding:utf-8 -*-

from . import core, loader
from . import constants as c
from engine.scenario import main_menu, levels


def main():
    """ """
    engine = core.EngineCore(loader.GAME_CAPTION)
    game_state_dict = {
        c.MAIN_MENU: main_menu.Menu(),
        c.INSTRUCTIONS: main_menu.Instructions(),
        c.LOADGAME: main_menu.LoadGame(),
        c.OVERWORLD: levels.LevelState(c.OVERWORLD)
    }
    engine.startup(game_state_dict, c.MAIN_MENU)
    engine.run()
