# -*- coding: utf-8 -*-

import libtcodpy as lbtc
from input_handlers import handle_keys
from entity import Entity
from render_functions import clear_all, render_all
from map_objects.game_map import GameMap

def main():
    screen_width = 80
    screen_height = 50
    map_width = 80
    map_height = 45
    
    colors = {
        'dark_wall': lbtc.Color(0, 0, 100),
        'dark_ground': lbtc.Color(50, 50, 150)
    
    }
    
    player = Entity(int(screen_width/2), int(screen_height/2), '@', lbtc.white)
    npc = Entity(int(screen_width/2 - 5), int(screen_height/2), '@', lbtc.yellow)
    entities = [npc, player]
    
    
    lbtc.console_set_custom_font('arial10x10.png', lbtc.FONT_TYPE_GRAYSCALE | lbtc.FONT_LAYOUT_TCOD)
    lbtc.console_init_root(screen_width, screen_height, 'libtcod tutorial revised', False)
    
	#console which we are working with to make new consoles in the future
    con = lbtc.console_new(screen_width, screen_height)
    
    game_map = GameMap(map_width, map_height)
    
    key = lbtc.Key()
    mouse = lbtc.Mouse()
    
    while not lbtc.console_is_window_closed():
        lbtc.sys_check_for_event(lbtc.EVENT_KEY_PRESS, key, mouse)
        
        render_all(con, entities, game_map, screen_width, screen_height, colors)
        lbtc.console_flush()
        
        clear_all(con, entities)
        
        action = handle_keys(key)

        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        if move:
            dx,dy = move
            if not game_map.is_blocked(player.x + dx, player.y + dy):
                player.move(dx, dy)
            
        if exit:
            return True

        if fullscreen:
            lbtc.console_set_fullscreen(not lbtc.console_is_fullscreen())

        #lbtc.console_delete(0)

if __name__ == '__main__':
    main()
    
