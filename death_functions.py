import tcod as libtcod

from game_states import GameStates
from render_functions import RenderOrder


def kill_monster(monster):
    death_message = f'{monster.name.capitalize()} is dead!'

    monster.char = '%'
    monster.color = libtcod.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = f'remains of {monster.name.capitalize()}'
    monster.render_order = RenderOrder.CORPSE

    return death_message


def kill_player(player):
    player.char = '%'
    player.color = libtcod.dark_red

    return 'You died!', GameStates.PLAYER_DEAD
