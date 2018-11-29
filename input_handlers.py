# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 09:36:11 2018

@author: tamir
"""

import libtcodpy as lbtc

def handle_keys(key):
    #Movement Keys
    if key.vk == lbtc.KEY_UP:
        return {'move': (0,-1)}
    elif key.vk == lbtc.KEY_DOWN:
        return {'move': (0,1)}
    elif key.vk == lbtc.KEY_LEFT:
        return {'move': (-1,0)}
    elif key.vk == lbtc.KEY_RIGHT:
        return {'move': (1,0)}

    if key.vk == lbtc.KEY_ENTER and key.lalt:
        #Alt+Enter: toggle full screen
        return {'fullscreen': True}
    elif key.vk == lbtc.KEY_ESCAPE:
        #Exit the game
        return {'exit': True}
    
    #No key Pressed
    return{}