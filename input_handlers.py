import tcod as libtcod

from game_states import GameStates


def handle_keys(key, game_state):
    if game_state == GameStates.PLAYERS_TURN:
        return handle_player_turn_keys(key)
    elif game_state == GameStates.PLAYER_DEAD:
        return handle_player_dead_keys(key)
    elif game_state in [GameStates.DROP_INVENTORY, GameStates.SHOW_INVENTORY]:
        return handle_inventory_keys(key)

    return {}


def handle_inventory_keys(key):
    index = key.c - ord('a')

    if index >= 0:
        return {'inventory_index': index}

    elif key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        # exit the menu
        return {'exit': True}

    return {}


def handle_player_dead_keys(key):
    key_char = chr(key.c)

    if key_char == '1':
        return {'show_inventory': True}
    elif key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        # exit the menu
        return {'exit': True}

    return {}


def handle_player_turn_keys(key):
    key_char = chr(key.c)

    # movement keys
    if key.vk == libtcod.KEY_UP or key_char == 'k':
        return {"move": (0, -1)}
    elif key.vk == libtcod.KEY_DOWN or key_char == 'j':
        return {"move": (0, 1)}
    elif key.vk == libtcod.KEY_LEFT or key_char == 'h':
        return {"move": (-1, 0)}
    elif key.vk == libtcod.KEY_RIGHT or key_char == 'l':
        return {"move": (1, 0)}
    elif key_char == 'y':
        return {'move': (-1, -1)}
    elif key_char == 'u':
        return {'move': (1, -1)}
    elif key_char == 'b':
        return {'move': (-1, 1)}
    elif key_char == 'n':
        return {'move': (1, 1)}

    elif key_char == 'g':
        return {'pickup': True}

    elif key_char == 'i':
        return {'show_inventory': True}

    elif key_char == 'd':
        return {'drop_inventory': True}

    elif key.vk == libtcod.KEY_ENTER and key.lalt:
        # alt+enter for fullscreen
        return {"fullscreen": True}
    elif key.vk == libtcod.KEY_ESCAPE:
        return {"exit": True}

    # handle no keypress
    return {}
