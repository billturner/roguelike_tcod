import os
import shelve
from typing import List, Tuple

from game_states import GameStates
from components.entity import Entity
from components.message_log import MessageLog
from map_objects.game_map import GameMap


def load_game() -> Tuple:
    if not os.path.isfile('data/savegame.dat'):
        # TODO: show the error in a better way
        raise FileNotFoundError

    # open up the shelve data file to read in previous game state
    with shelve.open('data/savegame', 'r') as data_file:
        player_index = data_file['player_index']
        entities = data_file['entities']
        game_map = data_file['game_map']
        message_log = data_file['message_log']
        game_state = data_file['game_state']

    player = entities[player_index]

    return player, entities, game_map, message_log, game_state


def save_game(player: Entity, entities: List[Entity], game_map: GameMap,
              message_log: MessageLog, game_state: GameStates) -> None:
    # create data directory if it does not yet exist
    if not os.path.exists('./data'):
        os.makedirs('./data')

    # write the current game state to the savegame file
    # TODO: how about in
    with shelve.open('data/savegame', 'n') as data_file:
        data_file['player_index'] = entities.index(player)
        data_file['entities'] = entities
        data_file['game_map'] = game_map
        data_file['message_log'] = message_log
        data_file['game_state'] = game_state
