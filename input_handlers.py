import libtcodpy as lbtc

from game_states import GameStates

'''
What does this do?
returns dictionaries that when analyzed makes other functions do stuff
here he accepts the input from user and depending on which game state the game is
he returns the corresponding action of the player
'''

def handle_keys(key, game_state):
    if game_state == GameStates.PLAYERS_TURN:
        return handle_player_turn_keys(key)
    elif game_state == GameStates.PLAYER_DEAD:
        return handle_player_dead_keys(key)
    elif game_state == GameStates.TARGETING:
        return handle_targeting_keys(key)
    elif game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        return handle_inventory_keys(key)
    elif game_state == GameStates.LEVEL_UP:
        return handle_level_up_menu(key)
    elif game_state == GameStates.CHARACTER_SCREEN:
        return handle_character_screen(key)

        
    return {}

def handle_player_turn_keys(key):
    key_char = chr(key.c)

    #Movement Keys
    if key.vk == lbtc.KEY_UP or key.vk == lbtc.KEY_KP8:
        return {'move': (0,-1)}#UP
    elif key.vk == lbtc.KEY_DOWN or key.vk == lbtc.KEY_KP2:
        return {'move': (0,1)}#DOWN
    elif key.vk == lbtc.KEY_LEFT or key.vk == lbtc.KEY_KP4:
        return {'move': (-1,0)}#LEFT
    elif key.vk == lbtc.KEY_RIGHT or key.vk == lbtc.KEY_KP6:
        return {'move': (1,0)}#RIGHT
        #Diagonals
    elif key.vk == lbtc.KEY_KP3:
        return {'move': (1,1)}# DOWN RIGHT
    elif key.vk == lbtc.KEY_KP9:
        return {'move': (1,-1)}# UP RIGHT
    elif key.vk == lbtc.KEY_KP1:
        return {'move': (-1,1)}# DOWN LEFT
    elif key.vk == lbtc.KEY_KP7:
        return {'move': (-1,-1)}# UP LEFT
    
    #Pass turn / Wait
    elif key.vk == lbtc.KEY_KP5 or key_char == 'w':
        return {'wait': True}

    
    #Action Keys
    #GRAB
    elif key_char == 'g':
        return {'pickup': True}
    #INVENTORY ACCESS
    elif key_char == 'i':
        return{'show_inventory': True}
    #DROP
    elif key_char == 'd':
        return{'drop_inventory': True}
    #GO DOWN THE STAIRS
    elif key.vk == lbtc.KEY_ENTER:
        return {'take_stairs': True}
    
    #UI Screens
    elif key_char == 'c':
        return{'show_character_screen': True}
        
        
    #Game stuff keys
    if key.vk == lbtc.KEY_ENTER and key.lalt:
        #Alt+Enter: toggle full screen
        return {'fullscreen': True}
    elif key.vk == lbtc.KEY_ESCAPE:
        #Exit the game
        return {'exit': True}
    
    #No key Pressed
    return{}
    
def handle_targeting_keys(key):
    if key.vk == lbtc.KEY_ESCAPE:
        return{'exit': True}
        
    return {}
    
def handle_inventory_keys(key):
    index = key.c - ord('a')
    
    if index >= 0:
        return {'inventory_index': index}
        
    if key.vk == lbtc.KEY_ENTER and key.lalt:
        #alt+enter : toggle full screen
        return {'fullscreen': True}
    elif key.vk == lbtc.KEY_ESCAPE:
        #Exits the menu
        return {'exit': True}
        
    return {}

def handle_main_menu(key):
    key_char = chr(key.c)
    
    if key_char == 'a':
        return {'new_game': True}
    elif key_char == 'b':
        return {'load_game': True}
    elif key_char == 'c' or key.vk == lbtc.KEY_ESCAPE:
        return{'exit': True}
    
    return{}
    
def handle_player_dead_keys(key):
    key_char = chr(key.c)
    
    if key_char == 'i':
        return {'show_inventory': True}
        
    if key.vk == lbtc.KEY_ENTER and key.lalt:
        #Alt + Enter: toggle full screen
        return {'fullscreen': True}
    elif key.vk == lbtc.KEY_ESCAPE:
        #Exits the menu
        return {'exit': True}
        
    return {}
    
def handle_level_up_menu(key):
    if key:
        key_char = chr(key.c)
        
        if key_char == 'a' or key.vk == lbtc.KEY_KP1:
            return {'level_up': 'hp'}
        elif key_char == 'b' or key.vk == lbtc.KEY_KP2:
            return {'level_up': 'str'}
        elif key_char == 'c' or key.vk == lbtc.KEY_KP3:
            return {'level_up': 'def'}
    
    return{}
    
def handle_character_screen(key):
    if key.vk == lbtc.KEY_ESCAPE:
        return{'exit': True}
        
    return{}
    
def handle_mouse(mouse):
    (x, y) = (mouse.cx, mouse.cy)
    
    if mouse.lbutton_pressed:
        return{'left_click': (x, y)}
    elif mouse.rbutton_pressed:
        return {'right_click': (x, y)}
        
    return {}
    
    
    
    
    
    