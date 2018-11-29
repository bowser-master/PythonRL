# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 09:36:11 2018

@author: tamir
"""

import libtcodpy as lbtc

def handle_keys(key):
    #Movement Keys
    if key.vk == lbtc.KEY_UP or key.vk == lbtc.KEY_KP8:
        return {'move': (0,-1)}
    elif key.vk == lbtc.KEY_DOWN or key.vk == lbtc.KEY_KP2:
        return {'move': (0,1)}
    elif key.vk == lbtc.KEY_LEFT or key.vk == lbtc.KEY_KP4:
        return {'move': (-1,0)}
    elif key.vk == lbtc.KEY_RIGHT or key.vk == lbtc.KEY_KP6:
        return {'move': (1,0)}
        #Diagonals
    elif key.vk == lbtc.KEY_KP3:
        return {'move': (1,1)}
    elif key.vk == lbtc.KEY_KP9:
        return {'move': (1,-1)}
    elif key.vk == lbtc.KEY_KP1:
        return {'move': (-1,1)}
    elif key.vk == lbtc.KEY_KP7:
        return {'move': (-1,-1)}

    if key.vk == lbtc.KEY_ENTER and key.lalt:
        #Alt+Enter: toggle full screen
        return {'fullscreen': True}
    elif key.vk == lbtc.KEY_ESCAPE:
        #Exit the game
        return {'exit': True}
    
    #No key Pressed
    return{}