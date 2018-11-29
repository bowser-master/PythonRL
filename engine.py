# -*- coding: utf-8 -*-

import libtcodpy as lbtc
from input_handlers import handle_keys

def main():
    screen_width = 80
    screen_height = 50
    
    player_x = int(screen_width/2)
    player_y = int(screen_height/2)
    
    lbtc.console_set_custom_font('arial10x10.png', lbtc.FONT_TYPE_GRAYSCALE | lbtc.FONT_LAYOUT_TCOD)
    lbtc.console_init_root(screen_width, screen_height, 'libtcod tutorial revised', False)
    
	#console which we are working with to make new consoles in the future
    con = lbtc.console_new(screen_width, screen_height)
    key = lbtc.Key()
    mouse = lbtc.Mouse()
    
    while not lbtc.console_is_window_closed():
        lbtc.sys_check_for_event(lbtc.EVENT_KEY_PRESS, key, mouse)
        
        
        lbtc.console_set_default_foreground(con, lbtc.white)
        lbtc.console_put_char(con, player_x, player_y, '@', lbtc.BKGND_NONE)
        lbtc.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)
        lbtc.console_flush()
        
        lbtc.console_put_char(con, player_x, player_y, ' ', lbtc.BKGND_NONE)

        action = handle_keys(key)

        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        if move:
            dx,dy = move
            player_x += dx
            player_y += dy

        if exit:
            return True

        if fullscreen:
            lbtc.console_set_fullscreen(not lbtc.console_is_fullscreen())

        #lbtc.console_delete(0)

if __name__ == '__main__':
    main()
    
