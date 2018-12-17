import math
import libtcodpy as lbtc

from render_functions import RenderOrder

'''
What does this do?
This creates the framework to build things in our world, things that have
position (x, y), a character representation with color, a name, if it blocks, render_order
if its a fighter, if it has ai, if its an item, and inventory?
Has some basic functions
move, move_towards, move_astar, distance, distance_to, and outside the entity class there is
get_blocking_entities_at_location

So it handles pretty basic stuff that almost everyone will have
'''

class Entity:
    ''' 
    A generic object to represent players, enemies, items, etc.
    Inputs: x, y (positions), character, color, name, optionals: blocks, fighter, ai
    '''
    def __init__(self, x, y, char, color, name, blocks=False, render_order=RenderOrder.CORPSE,
        fighter=None, ai=None, item=None, inventory=None, stairs=None, level=None):
        '''
            here are all the info on entities that they will carry.
            x, y, character representation, color, name, blocks=False, render_order=RenderOrder.CORPSE,
            fighter=None, ai=None, item=None, inventory=None, stairs=None
        '''
        self.x = x
        self.y = y
        self.char = char
        self.color = color 
        self.name = name
        self.blocks = blocks
        self.render_order = render_order
        self.fighter = fighter
        self.ai = ai
        self.item = item
        self.inventory = inventory
        self.stairs = stairs
        self.level = level
        
        if self.fighter:
            self.fighter.owner = self
            
        if self.ai:
            self.ai.owner = self
        
        if self.item:
            self.item.owner = self
            
        if self.inventory:
            self.inventory.owner = self
            
        if self.stairs:
            self.stairs.owner = self
            
        if self.level:
            self.level.owner = self
        
    def move(self, dx, dy):
        '''
            Simply makes someone move given the amount for x and y (dx, dy)
        '''
        #Move the entity by a given amount
        self.x += dx
        self.y += dy
        
    def move_towards(self, target_x, target_y, game_map, entities):
        '''
            makes an entity move toward something, given target_x and _y, the game_map and entities
        '''
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        
        dx = int(round(dx/distance))
        dy = int(round(dy/distance))
        
        if not (game_map.is_blocked(self.x + dx, self.y +dy) or  
                    get_blocking_entities_at_location(entities, self.x + dx, self.y + dy)):
            self.move(dx, dy)
            
    def move_astar(self, target, entities, game_map):
        '''
            Makes it so you travel the fastest path from one place to another
        '''
        # Create a FOV map that has the dimensions of the map
        fov = lbtc.map_new(game_map.width, game_map.height)

        # Scan the current map each turn and set all the walls as unwalkable
        for y1 in range(game_map.height):
            for x1 in range(game_map.width):
                lbtc.map_set_properties(fov, x1, y1, not game_map.tiles[x1][y1].block_sight,
                                           not game_map.tiles[x1][y1].blocked)

        # Scan all the objects to see if there are objects that must be navigated around
        # Check also that the object isn't self or the target (so that the start and the end points are free)
        # The AI class handles the situation if self is next to the target so it will not use this A* function anyway
        for entity in entities:
            if entity.blocks and entity != self and entity != target:
                # Set the tile as a wall so it must be navigated around
                lbtc.map_set_properties(fov, entity.x, entity.y, True, False)

        # Allocate a A* path
        # The 1.41 is the normal diagonal cost of moving, it can be set as 0.0 if diagonal moves are prohibited
        my_path = lbtc.path_new_using_map(fov, 1.41)

        # Compute the path between self's coordinates and the target's coordinates
        lbtc.path_compute(my_path, self.x, self.y, target.x, target.y)

        # Check if the path exists, and in this case, also the path is shorter than 25 tiles
        # The path size matters if you want the monster to use alternative longer paths (for example through other rooms) if for example the player is in a corridor
        # It makes sense to keep path size relatively low to keep the monsters from running around the map if there's an alternative path really far away
        if not lbtc.path_is_empty(my_path) and lbtc.path_size(my_path) < 25:
            # Find the next coordinates in the computed full path
            x, y = lbtc.path_walk(my_path, True)
            if x or y:
                # Set self's coordinates to the next path tile
                self.x = x
                self.y = y
        else:
            # Keep the old move function as a backup so that if there are no paths (for example another monster blocks a corridor)
            # it will still try to move towards the player (closer to the corridor opening)
            self.move_towards(target.x, target.y, game_map, entities)

            # Delete the path to free memory
        lbtc.path_delete(my_path)
        
    def distance(self, x, y):
        '''
        Measures the distance from self to any x, y space
        '''
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)
            
    def distance_to(self, other):
        '''
            Measures the distance of 2 entities, from self to other, only gets 1 var = other entity 
        '''
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)
        
    
def get_blocking_entities_at_location(entities, destination_x, destination_y):
        '''
            Pretty self explanatory, checks on a destination_x and _y if an entity is blocking the way
        '''
        for entity in entities:
            if entity.blocks and entity.x == destination_x and entity.y == destination_y:
                return entity
                
        return None
        