import libtcodpy as lbtc

from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from components.equipment import Equipment

from misc.entity import Entity

from game_things.game_messages import MessageLog
from game_things.game_states import GameStates

from map_objects.game_map import GameMap

from functions.render_functions import RenderOrder

def get_constants():
    window_title = 'Roguelike Tut'
    
    #Screen Variables 
    screen_width = 100 #was 80
    screen_height = 62 #was 50
    
    #Panel Variables
    bar_width = screen_width//4
    panel_width = screen_width//4
    panel_height = 7
    panel_y = 0 #was screen_height - panel_height
    
    #Sidebar Variables
    sidebar_width = screen_width//4
    sidebar_height = screen_height
    sidebar_x = screen_width - sidebar_width
    
    #Map Variables
    map_width = 3*screen_width//4
    map_y = 7
    map_height = 43
    
    #Message
    message_x = sidebar_width + 2
    message_width = sidebar_width - 1
    message_height = sidebar_height - 1
    
    #Rooms Variables
    room_max_size = 10
    room_min_size = 6
    max_rooms = 30
    
    #FOV Variables
    fov_algorithm = 0 #will be used for lbtc. fov algorithm
    fov_light_walls = True #wether or not it lights up the walls we see
    fov_radius = 10 #Self explanatory
    
    #Entities Variables
    max_monsters_per_room = 6
    max_items_per_room = 15
    
    colors = {
        'dark_wall': lbtc.Color(0, 0, 100),
        'dark_ground': lbtc.Color(50, 50, 150),
        'light_wall': lbtc.Color(130, 110, 50),
        'light_ground': lbtc.Color(200, 180, 50)
    
    }
    
    constants = {
        'window_title': window_title,
        'screen_width': screen_width,
        'screen_height': screen_height,
        'map_width': map_width,
        'map_height': map_height,
        'bar_width': bar_width,
        'panel_width': panel_width,
        'panel_height': panel_height,
        'panel_y': panel_y,
        'sidebar_height': sidebar_height,
        'sidebar_width': sidebar_width,
        'sidebar_x': sidebar_x,
        'message_x': message_x,
        'message_width': message_width,
        'message_height': message_height,        
        'room_max_size': room_max_size,
        'room_min_size': room_min_size,
        'max_rooms': max_rooms,
        'fov_algorithm': fov_algorithm,
        'fov_light_walls': fov_light_walls,
        'fov_radius': fov_radius,
        'max_monsters_per_room': max_monsters_per_room,
        'max_items_per_room': max_items_per_room,
        'colors': colors
    }

    return constants
    
def get_game_variables(constants):

    fighter_component = Fighter(hp=30, defense=2, power=5)
    inventory_component = Inventory(26)
    level_component = Level()
    equipment_component = Equipment()
    player = Entity(0, 0, '@', lbtc.white, 'Player', blocks=True, render_order=RenderOrder.ACTOR,
                fighter=fighter_component, inventory=inventory_component, level=level_component,
                equipment=equipment_component)
                
    entities = [player]
    
    game_map = GameMap(constants['map_width'], constants['map_height'])
    game_map.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'],
                    constants['map_width'], constants['map_height'], player, entities)
    message_log = MessageLog(constants['message_x'], constants['message_width'], constants['message_height'])

    game_state = GameStates.PLAYERS_TURN
    
    return player, entities, game_map, message_log, game_state
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    