import libtcodpy as lbtc

from game_things.game_states import GameStates
from game_things.play_game import play_game
from game_things.menus import main_menu, message_box

from loader_functions.initialize_new_game import get_constants, get_game_variables
from loader_functions.data_loaders import load_game, save_game

from misc.input_handlers import handle_main_menu

'''
This is our main executable file that manages our stuff
game loop moved to play_game.py which is called here
'''
def main():
    constants = get_constants()
    
    lbtc.console_set_custom_font('arial10x10.png', lbtc.FONT_TYPE_GRAYSCALE | lbtc.FONT_LAYOUT_TCOD)
    
    lbtc.console_init_root(constants['screen_width'], constants['screen_height'], constants['window_title'], False)
    
	#console which we are working with to make new consoles in the future
    con = lbtc.console_new(constants['screen_width'], constants['screen_height'])
    #character stuff panel ?
    panel = lbtc.console_new(constants['panel_width'], constants['panel_height'])
    #sidebar stuff
    sidebar = lbtc.console_new(constants['sidebar_width'], constants['sidebar_height'])
    
    player = None
    entities = []
    game_map = None
    message_log = None
    game_state = None
    
    show_main_menu = True
    show_load_error_message = False
    
    main_menu_background_image = lbtc.image_load('menu_background.png')
    
    key = lbtc.Key()
    mouse = lbtc.Mouse()
    
    while not lbtc.console_is_window_closed():
        lbtc.sys_check_for_event(lbtc.EVENT_KEY_PRESS | lbtc.EVENT_MOUSE, key, mouse)
        
        if show_main_menu:
            main_menu(con, main_menu_background_image, constants['screen_width'],constants['screen_height'])
            
            if show_load_error_message:
                message_box(con, 'No save game to load', 50, constants['screen_width'], constants['screen_height'])
            
            lbtc.console_flush()
            
            action = handle_main_menu(key)
            
            new_game = action.get('new_game')
            load_saved_game = action.get('load_game')
            exit_game = action.get('exit')
            
            if show_load_error_message and (new_game or load_saved_game or exit_game):
                show_load_error_message = False
            elif new_game:
                player, entities, game_map, message_log, game_state = get_game_variables(constants)
                game_state = GameStates.PLAYERS_TURN
                
                show_main_menu = False
                
            elif load_saved_game:
                try:
                    player, entities, game_map, message_log, game_state = load_game()
                    show_main_menu = False
                except FileNotFoundError:
                    show_load_error_message = True
            elif exit_game:
                break
        else:
            lbtc.console_clear(con)
            play_game(player, entities, game_map, message_log, game_state, con, panel, sidebar, constants)
            
            show_main_menu = True
                

if __name__ == '__main__':
    main()
    
