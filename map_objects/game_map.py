import libtcodpy as lbtc
from random import randint

from components.ai import BasicMonster
from components.fighter import Fighter
from components.item import Item
from components.stairs import Stairs
from components.equipment import EquipmentSlots
from components.equippable import Equippable

from functions.item_functions import heal, cast_lightning, cast_fireball, cast_confuse
from functions.render_functions import RenderOrder

from game_things.game_messages import Message

from misc.random_utils import random_choice_from_dict, from_dungeon_level
from misc.entity import Entity

from map_objects.rectangle import Rect
from map_objects.tile import Tile

'''
What does this do?
Creates the game map (but doesn't draw it), with all creatures, tiles and items in the dungeon
for now is a pretty simple version but that's what we got

functions: initialize_tiles, make_map (only creates the map) using other functions like (create_room, create_h and v_tunnel)
place_entities (now he puts entities (randomly in the dungeon)), is_blocked (checks if tile is blocked)
'''

class GameMap:
    def __init__(self, width, height, dungeon_level=1):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()
        self.dungeon_level = dungeon_level
        
    def to_json(self):
        json_data = {
            'width': self.width,
            'height': self.height,
            'tiles': [[tile.to_json() for tile in tile_rows] for tile_rows in self.tiles]
        }

        return json_data

    @staticmethod
    def from_json(json_data):
        width = json_data.get('width')
        height = json_data.get('height')
        tiles_json = json_data.get('tiles')

        game_map = GameMap(width, height)
        game_map.tiles = Tile.from_json(tiles_json)

        return game_map
        
    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]
        return tiles
        
    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height,
                 player, entities):
        #random created dungeon!
        
        rooms = []
        num_rooms = 0
        
        center_of_last_room_x = None
        center_of_last_room_y = None
        
        for r in range(max_rooms):
            #random width and height
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)
            #random position without going out of bounds of the map
            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h - 1)
            
            #Rect class makes rectangles easier to work with
            new_room = Rect(x, y, w, h)
            
            #run through the other rooms and see if they intersect with this one
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
                
            else:
                #this means there are no intersections, so this room is valid
                
                #paint it to the maps's tiles
                self.create_room(new_room)
                
                #center coordinates of new room, will be useful later
                (new_x, new_y) = new_room.center()
                
                center_of_last_room_x = new_x
                center_of_last_room_y = new_y
                
                if num_rooms == 0:
                    #this is the first room, where the player starts at
                    player.x = new_x
                    player.y = new_y
                else:
                    #all rooms after the first:
                    #connect it to the previous room with a tunnel
                    
                    #center coordinates of previous room
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()
                    
                    #flip a coin (random num that is either 0 or 1)
                    if randint(0, 1) == 1:
                        #first move horizontally, then vertically
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        #first move vertically then horizontally
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)
                        
                self.place_entities(new_room, entities)
                        
                #finally, append the new room to the list
                rooms.append(new_room)
                num_rooms += 1
        
        stairs_component = Stairs(self.dungeon_level + 1)
        down_stairs = Entity(center_of_last_room_x, center_of_last_room_y, '>', lbtc.white, 'Stairs',
                        render_order=RenderOrder.STAIRS, stairs=stairs_component)
        entities.append(down_stairs)


       
    def create_room(self, room):
        #go through the tiles in the rectangle and make them passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 +1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False
                
    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False
        
    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False
            
    def place_entities(self, room, entities):
        
        max_monsters_per_room = from_dungeon_level([[2, 1], [3, 4], [5, 6]], self.dungeon_level)
        max_items_per_room = from_dungeon_level([[1, 1], [2, 4]], self.dungeon_level)
        
        #get a random number of monsters
        number_of_monsters = randint(0, max_monsters_per_room)
        number_of_items = randint(0, max_items_per_room)
        
        monster_chances = {
            'orc': 80,
            'troll': from_dungeon_level([[15, 3], [30, 5], [60, 7]], self.dungeon_level)
        }
            
        item_chances = {
        'healing_potion': 10,
        'sword': from_dungeon_level([[900, 1]], self.dungeon_level),
        'shield': from_dungeon_level([[900, 1]], self.dungeon_level),
        'lightning_scrool': from_dungeon_level([[25, 1]], self.dungeon_level),
        'fireball_spell': from_dungeon_level([[25, 1]], self.dungeon_level),
        'confusion_scroll': from_dungeon_level([[10, 1]], self.dungeon_level)
        }
        
        #Creating MONSTERS
        for i in range(number_of_monsters):
            #choose a random location in the room
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)
            
            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                monster_choice = random_choice_from_dict(monster_chances)
                
                if monster_choice == 'orc':
                    figther_component = Fighter(hp=10, defense=0, power=3, xp=100)
                    ai_component = BasicMonster()
                    
                    monster = Entity(x, y, 'o', lbtc.desaturated_green, 'Orc', blocks=True, 
                                   render_order=RenderOrder.ACTOR, fighter=figther_component, ai=ai_component)
                else:
                    figther_component = Fighter(hp=16, defense=1, power=4, xp=200)
                    ai_component = BasicMonster()
                    monster = Entity(x, y, 'T', lbtc.darker_green, 'Troll', blocks=True, 
                                   render_order=RenderOrder.ACTOR, fighter=figther_component, ai=ai_component)
                    
                entities.append(monster)
                
        #Creating Items        
        for i in range(number_of_items):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)
            
            if not any ([entity for entity in entities if entity.x == x and entity.y == y]):
                item_choice = random_choice_from_dict(item_chances)
                
                #Just an item randomizer for making it
                if item_choice == 'healing_potion':
                    item_component = Item(use_function=heal, amount=4)
                    item = Entity(x, y, '!', lbtc.violet, 'Healing Potion', 
                            render_order=RenderOrder.ITEM, item=item_component)
                
                elif item_choice == 'sword':
                    equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=3)
                    item = Entity(x, y, '/', lbtc.sky, 'Sword', equippable=equippable_component)
                
                elif item_choice == 'shield':
                    equippable_component = Equippable(EquipmentSlots.OFF_HAND, defense_bonus=1)
                    item = Entity(x, y, '[', lbtc.darker_orange, 'Shield', equippable=equippable_component)
                
                elif item_choice == 'lightning_scroll':
                    item_component = Item(use_function=cast_lightning, damage=20, maximum_range=5)
                    item = Entity(x, y, '#', lbtc.yellow, 'Lightning Scroll', render_order=RenderOrder.ITEM,
                                item=item_component)
                
                elif item_choice == 'fireball_scroll':
                    item_component = Item(use_function=cast_fireball, targeting=True, targeting_message=Message(
                            'Left-click a target tile for the fireball, or right-click to cancel.', lbtc.light_cyan),
                            damage=12, radius=3)
                    item = Entity(x, y, '#', lbtc.red, 'Fireball Scroll', render_order=RenderOrder.ITEM,
                            item=item_component)
                
                else:
                    item_component = Item(use_function=cast_confuse, targeting=True, targeting_message=Message(
                            'Left-click an enemy to confuse it, or right-click to cancel.', lbtc.light_cyan))
                    item = Entity(x, y, '#', lbtc.light_pink, 'Confusion Scroll', render_order=RenderOrder.ITEM,
                                    item=item_component)
                
                
                entities.append(item)
        
    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True
            
        return False
        
    def next_floor(self, player, message_log, constants):
        self.dungeon_level += 1
        entities = [player]
        
        self.tiles = self.initialize_tiles()
        self.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'],
                      constants['map_width'], constants['map_height'], player, entities)
        
        player.fighter.heal(player.fighter.max_hp // 2)
        
        message_log.add_message(Message('You take a moment to rest, and recover your strength.', lbtc.light_violet))
        
        return entities
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        