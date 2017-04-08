#!/usr/bin/env python
# -*- coding:utf-8 -*-

from . import loader

class Subscriber(object):
    def __init__(self):
        pass

    def on_notify(self, event):
        pass


class Publisher(object):
    def __init__(self):
        self.subscribers = set()

    def register(self, who):
        self.subscribers.add(who)

    def unregister(self, who):
        self.subscribers.discard(who)

    def dispatch(self, event):
        for subscriber in self.subscribers:
            subscriber.on_notify(event)

class SoundEffects(object):
    """
    Observer for sound effects
    """
    def on_notify(self, event):
        if event in loader.SFX:
            loader.SFX[event].play()