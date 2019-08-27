import tcod
from typing import Dict, Tuple

from components.entity import Entity
from components.equipment import Equipment
from components.equippable import Equippable
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from components.message_log import MessageLog
from constants.equipment_slots import EquipmentSlots
from constants.game_states import GameStates
from functions.render import RenderOrder
from map_objects.game_map import GameMap


def get_constants() -> Dict:
    window_title: str = 'Roguelike Tutorial tcod'

    screen_width: int = 80
    screen_height: int = 50

    bar_width: int = 20
    panel_height: int = 7
    panel_y: int = screen_height - panel_height

    message_x: int = bar_width + 2
    message_width: int = screen_width - bar_width - 2
    message_height: int = panel_height - 1

    map_width: int = 80
    map_height: int = 43

    room_max_size: int = 10
    room_min_size: int = 6
    max_rooms: int = 30

    fov_algorithm: int = 0
    fov_light_walls: bool = True
    fov_radius: int = 10

    max_monsters_per_room: int = 3
    max_items_per_room: int = 2

    colors: Dict = {
        'dark_wall': tcod.Color(169, 169, 169),  # CSS DarkGray
        'dark_ground': tcod.Color(0, 0, 0),  # CSS Black
        'light_wall': tcod.Color(130, 110, 50),
        'light_ground': tcod.Color(200, 180, 50),
        'player': tcod.white,
        'magic_item': tcod.violet,
        'orc': tcod.desaturated_green,
        'troll': tcod.darker_green
    }

    constants: Dict = {
        'window_title': window_title,
        'screen_width': screen_width,
        'screen_height': screen_height,
        'bar_width': bar_width,
        'panel_height': panel_height,
        'panel_y': panel_y,
        'message_x': message_x,
        'message_width': message_width,
        'message_height': message_height,
        'map_width': map_width,
        'map_height': map_height,
        'room_max_size': room_max_size,
        'room_min_size': room_min_size,
        'max_rooms': max_rooms,
        'fov_algorithm': fov_algorithm,
        'fov_light_walls': fov_light_walls,
        'fov_radius': fov_radius,
        'max_monsters_per_room': max_monsters_per_room,
        'max_items_per_room': max_items_per_room,
        'colors': colors
    }

    return constants


def get_game_variables(constants: Dict) -> Tuple:
    # initialize player/fighter and inventory
    fighter_component = Fighter(hp=100, defense=1, power=2)
    inventory_component = Inventory(26)
    level_component = Level()
    equipment_component = Equipment()
    player = Entity(int(constants['screen_width'] / 2),
                    int(constants['screen_height'] /
                        2), "@", constants['colors'].get('player'),
                    'Player', blocks=True, render_order=RenderOrder.ACTOR,
                    fighter=fighter_component, inventory=inventory_component,
                    level=level_component, equipment=equipment_component)
    entities = [player]

    # set up inventory stuff
    equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=2)
    dagger = Entity(0, 0, '-', tcod.sky, 'Dagger',
                    equippable=equippable_component)
    player.inventory.add_item(dagger)
    player.equipment.toggle_equip(dagger)

    # initialize game map
    game_map = GameMap(constants['map_width'], constants['map_height'])
    game_map.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'],
                      constants['map_width'], constants['map_height'], player,
                      entities, constants['colors'])

    # initialize blank message log
    message_log = MessageLog(
        constants['message_x'], constants['message_width'], constants['message_height'])

    # set initial game state
    game_state = GameStates.PLAYERS_TURN

    return player, entities, game_map, message_log, game_state
