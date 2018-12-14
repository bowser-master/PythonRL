import libtcodpy as lbtc

from enum import Enum


class RenderOrder(Enum):
    CORPSE = 1
    ITEM = 2
    ACTOR = 3

def render_all(con, entities, player, game_map, fov_map, fov_recompute, screen_width, screen_height, colors):
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
        draw_entity(con, entity, fov_map)
        
    lbtc.console_set_default_foreground(con, lbtc.white)
    lbtc.console_print_ex(con, 1, screen_height - 2, lbtc.BKGND_NONE, lbtc.LEFT,
                        'HP: {0:02}/{1:02}'. format(player.fighter.hp, player.fighter.max_hp))
    
    lbtc.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)
       
def clear_all(con, entities):
    #clears all entities!
    for entity in entities:
        clear_entity(con, entity)

def draw_entity(con, entity, fov_map):
    if lbtc.map_is_in_fov(fov_map, entity.x, entity.y):
        lbtc.console_set_default_foreground(con, entity.color)
        lbtc.console_put_char(con, entity.x, entity.y, entity.char, lbtc.BKGND_NONE)
     
def clear_entity(con, entity):
    #Erases the char that represents this object
    lbtc.console_put_char(con, entity.x, entity.y, ' ', lbtc.BKGND_NONE)