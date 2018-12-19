import libtcodpy as lbtc

from game_things.game_messages import Message
from game_things.game_states import GameStates

from functions.render_functions import RenderOrder



def kill_player(player):
    player.char = '%'
    player.color = lbtc.dark_red
    
    return Message('You died!'), GameStates.PLAYER_DEAD
    
    
def kill_monster(monster):
    death_message = Message('{0} is dead!'.format(monster.name.capitalize()), lbtc.orange)
    
    monster.char = '%'
    monster.color = lbtc.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = 'remains of ' + monster.name
    monster.render_order = RenderOrder.CORPSE
    
    return death_message