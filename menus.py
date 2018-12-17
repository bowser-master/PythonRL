import libtcodpy as lbtc


def menu(con, header, options, width, screen_width, screen_height):
    if len(options) > 26: raise ValueError('Cannot have a menu with more than 26 options, for now...')
    
    #calculate total height for the header (after auto-wrap) and one line per options
    header_height = lbtc.console_get_height_rect(con, 0, 0, width, screen_height, header)
    height = len(options) + header_height
    
    #create an off screen console that represents the menu's window
    window = lbtc.console_new(width, height)
    
    #print the header, with auto-wrap
    lbtc.console_set_default_foreground(window, lbtc.white)
    lbtc.console_print_rect_ex(window, 0, 0, width, height, lbtc.BKGND_NONE, lbtc.LEFT, header)
    
    #print all the options
    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = '('+ chr(letter_index) + ')' + option_text
        lbtc.console_print_ex(window, 0, y, lbtc.BKGND_NONE, lbtc.LEFT, text)
        y += 1
        letter_index += 1
        
    #blit the contents of "window" to the root console
    x = int(screen_width / 2 - width / 2)
    y = int(screen_height / 2 - height / 2)
    lbtc.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)
    
def inventory_menu(con, header, inventory, inventory_width, screen_width, scree_height):
    #show a menu with each item of the inventory as an option_text
    if len(inventory.items) == 0:
        options = ['Inventory is empty.']
    else:
        options = [item.name for item in inventory.items]
        
    menu(con, header, options, inventory_width, screen_width, scree_height)
    
def main_menu(con, background_image, screen_width, screen_height):
    lbtc.image_blit_2x(background_image, 0, 0, 0)
    
    lbtc.console_set_default_foreground(0, lbtc.light_yellow)
    lbtc.console_print_ex(0, int(screen_width/2), int(screen_height/2) - 4, lbtc.BKGND_NONE, lbtc.CENTER,
                            'COOL NAME HERE')
    lbtc.console_print_ex(0, int(screen_width/2), int(screen_height - 2), lbtc.BKGND_NONE, lbtc.CENTER,
                            'By Bowser Master')
                            
    menu(con, '', ['Play a new game', 'Continue last game', 'Quit'], 24, screen_width, screen_height)

def level_up_menu(con, header, player, menu_width, screen_width, screen_height):
    options = ['HP (+20 HP, from {0})'.format(player.fighter.max_hp),
               'ATK (+1 attack, from {0})'.format(player.fighter.power),
               'DEF (+1 defense, from {0})'.format(player.fighter.defense)]
    
    menu(con, header, options, width, screen_width, screen_height)
    
def character_screen(player, character_screen_width, character_screen_height, screen_width, scree_height):
    window = lbtc.console_new(character_screen_width, character_screen_height)
    
    lbtc.console_set_default_foreground(window, lbtc.white)
    
    lbtc.console_print_rect_ex(window, 0, 1, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Character Information')
    libtcod.console_print_rect_ex(window, 0, 2, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Level: {0}'.format(player.level.current_level))
    libtcod.console_print_rect_ex(window, 0, 3, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Experience: {0}'.format(player.level.current_xp))
    libtcod.console_print_rect_ex(window, 0, 4, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Experience to Level: {0}'.format(player.level.experience_to_next_level))
    libtcod.console_print_rect_ex(window, 0, 6, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Maximum HP: {0}'.format(player.fighter.max_hp))
    libtcod.console_print_rect_ex(window, 0, 7, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Attack: {0}'.format(player.fighter.power))
    libtcod.console_print_rect_ex(window, 0, 8, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Defense: {0}'.format(player.fighter.defense))
    
    x = screen_width // 2 - character_screen_width // 2
    y = screen_height // 2 - character_screen_height // 2
    lbtc.console_blit(window, 0, 0, character_screen_width, character_screen_height, 0, x, y, 1.0, 0.7)
    
def message_box(con, header, width, screen_width, scree_height):
    menu(con, header, [], width, screen_width, scree_height)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    