# -*- coding: utf-8 -*-

import libtcodpy as lbtc
from input_handlers import handle_keys
from entity import Entity, get_blocking_entities_at_location
from fov_functions import initialize_fov, recompute_fov
from game_states import GameStates
from render_functions import clear_all, render_all
from map_objects.game_map import GameMap

def main():
    #Screen Variables 
    screen_width = 80
    screen_height = 50
    map_width = 80
    map_height = 45
    
    #Rooms Variables
    room_max_size = 10
    room_min_size = 6
    max_rooms = 30
    
    #FOV Variables
    fov_algorithm = 0 #will be used for lbtc. fov algorithm
    fov_light_walls = True #wether or not it lights up the walls we see
    fov_radius = 10 #Self explanatory
    
    #Monsters Variables
    max_monsters_per_room = 3
    
    colors = {
        'dark_wall': lbtc.Color(0, 0, 100),
        'dark_ground': lbtc.Color(50, 50, 150),
        'light_wall': lbtc.Color(130, 110, 50),
        'light_ground': lbtc.Color(200, 180, 50)
    
    }
    
    player = Entity(0, 0, '@', lbtc.white, 'Player', blocks=True)
    entities = [player]
    
    
    lbtc.console_set_custom_font('arial10x10.png', lbtc.FONT_TYPE_GRAYSCALE | lbtc.FONT_LAYOUT_TCOD)
    lbtc.console_init_root(screen_width, screen_height, 'libtcod tutorial revised', False)
    
	#console which we are working with to make new consoles in the future
    con = lbtc.console_new(screen_width, screen_height)
    
    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room)
    
    fov_recompute = True #only computes FOV if the player moves! On by default cause we need it when game starts
    fov_map = initialize_fov(game_map)
    
    
    key = lbtc.Key()
    mouse = lbtc.Mouse()
    
    game_state = GameStates.PLAYERS_TURN
    
    while not lbtc.console_is_window_closed():
        lbtc.sys_check_for_event(lbtc.EVENT_KEY_PRESS, key, mouse)
        
        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)
        
        render_all(con, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colors)
        
        fov_recompute = False
        
        lbtc.console_flush()
        
        clear_all(con, entities)
        
        action = handle_keys(key)

        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        if move and game_state == GameStates.PLAYERS_TURN:
            dx,dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy
            
            if not game_map.is_blocked(destination_x, destination_y):
                target = get_blocking_entities_at_location(entities, destination_x, destination_y)
                
                if target:
                    print('You kick the '+target.name+ 'in the shins, much to its annoyance!')
                else:
                    player.move(dx, dy)
                    
                    fov_recompute = True
                    
                game_state = GameStates.ENEMY_TURN
                
        if exit:
            return True

        if fullscreen:
            lbtc.console_set_fullscreen(not lbtc.console_is_fullscreen())
            
        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity != player:
                    print('The ' +entity.name+ ' ponders the meaning of its existence.')
                    
            game_state = GameStates.PLAYERS_TURN

        #lbtc.console_delete(0)

if __name__ == '__main__':
    main()
    
