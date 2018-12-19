import libtcodpy as lbtc

from enum import Enum
from game_things.game_states import GameStates
from game_things.menus import inventory_menu, level_up_menu, character_screen


class RenderOrder(Enum):
    STAIRS = 1
    CORPSE = 2
    ITEM = 3
    ACTOR = 4

def get_names_under_mouse(mouse, entities, fov_map):
    (x, y) = (mouse.cx, mouse.cy)
    
    names = [entity.name for entity in entities
            if entity.x == x and entity.y == y and lbtc.map_is_in_fov(fov_map, entity.x, entity.y)]
            
    names = ', '.join(names)
    
    return names.capitalize()
    
def render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color):
    bar_width = int(float(value) / maximum * total_width )
    
    lbtc.console_set_default_background(panel, back_color)
    lbtc.console_rect(panel, x, y, total_width, 1, False, lbtc.BKGND_SCREEN)
    
    lbtc.console_set_default_background(panel, bar_color)
    if bar_width > 0:
        lbtc.console_rect(panel, x, y, bar_width, 1, False, lbtc.BKGND_SCREEN)
    
    lbtc.console_set_default_foreground(panel, lbtc.white)
    lbtc.console_print_ex(panel, int(x + total_width / 2), y, lbtc.BKGND_NONE, lbtc.CENTER,
                            '{0}: {1}/{2}'.format(name, value, maximum))
    
def render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log, screen_width, screen_height,
                bar_width, panel_height, panel_y, mouse, colors, game_state):
    #Draw all tiles in the game map
    if fov_recompute:
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = lbtc.map_is_in_fov(fov_map, x, y)
                wall = game_map.tiles[x][y].block_sight

                if visible:
                    if wall:
                        lbtc.console_set_char_background(con, x, y, colors.get('light_wall'), lbtc.BKGND_SET)
                    
                    else:
                        lbtc.console_set_char_background(con, x, y, colors.get('light_ground'), lbtc.BKGND_SET)
                    
                    game_map.tiles[x][y].explored = True
                
                elif game_map.tiles[x][y].explored:
                    if wall:
                        lbtc.console_set_char_background(con, x, y, colors.get('dark_wall'), lbtc.BKGND_SET)
                            
                    else:
                        lbtc.console_set_char_background(con, x, y, colors.get('dark_ground'), lbtc.BKGND_SET)
                
    entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value)
    
    #Draw all entities in the list
    for entity in entities_in_render_order:
        draw_entity(con, entity, fov_map, game_map)
        
    lbtc.console_set_default_foreground(panel, lbtc.black)

    lbtc.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)
    
    lbtc.console_set_default_background(panel, lbtc.black)
    lbtc.console_clear(panel)
    
    #Print the game messages, one line at a time
    y = 1
    for message in message_log.messages:
        lbtc.console_set_default_foreground(panel, message.color)
        lbtc.console_print_ex(panel, message_log.x, y, lbtc.BKGND_NONE, lbtc.LEFT, message.text)
        y += 1
    
    render_bar(panel, 1, 1, bar_width, 'HP', player.fighter.hp, player.fighter.max_hp,
                lbtc.light_red, lbtc.darker_red)
                
    lbtc.console_print_ex(panel, 1, 3, lbtc.BKGND_NONE, lbtc.LEFT, 
                            'Dungeon Level: {0}'.format(game_map.dungeon_level))
                
    lbtc.console_set_default_foreground(panel, lbtc.light_gray)
    lbtc.console_print_ex(panel, 1, 0, lbtc.BKGND_NONE, lbtc.LEFT,
                            get_names_under_mouse(mouse, entities, fov_map))
    
    lbtc.console_blit(panel, 0, 0, screen_width, panel_height, 0, 0, panel_y)
    
    if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        if game_state == GameStates.SHOW_INVENTORY:
            inventory_title = 'Press the key next to an item to use it, or Esc to cancel.\n'
        else:
            inventory_title = 'Press the key next to an item to drop it, or Esc to cancel.\n'
        
        inventory_menu(con, inventory_title, player, 50, screen_width, screen_height)
    
    elif game_state == GameStates.LEVEL_UP:
        level_up_menu(con, 'Level up! Choose a stat to raise: ', player, 40, screen_width, screen_height)
    
    elif game_state == GameStates.CHARACTER_SCREEN:
        character_screen(player, 30, 10, screen_width, screen_height)
        
def clear_all(con, entities):
    #clears all entities!
    for entity in entities:
        clear_entity(con, entity)

def draw_entity(con, entity, fov_map, game_map):
    if lbtc.map_is_in_fov(fov_map, entity.x, entity.y) or (entity.stairs and game_map.tiles[entity.x][entity.y].explored):
        lbtc.console_set_default_foreground(con, entity.color)
        lbtc.console_put_char(con, entity.x, entity.y, entity.char, lbtc.BKGND_NONE)
     
def clear_entity(con, entity):
    #Erases the char that represents this object
    lbtc.console_put_char(con, entity.x, entity.y, ' ', lbtc.BKGND_NONE)