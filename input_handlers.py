import tcod as libtcod


def handle_keys(key):
    # movement keys
    if key.vk == libtcod.KEY_UP:
        return {"move": (0, -1)}
    elif key.vk == libtcod.KEY_DOWN:
        return {"move": (0, 1)}
    elif key.vk == libtcod.KEY_LEFT:
        return {"move": (-1, 0)}
    elif key.vk == libtcod.KEY_RIGHT:
        return {"move": (1, 0)}

    # control keys
    elif key.vk == libtcod.KEY_ENTER and key.lalt:
        # alt+enter for fullscreen
        return {"fullscreen": True}
    elif key.vk == libtcod.KEY_ESCAPE:
        return {"exit": True}

    # handle no keypress
    return {}
