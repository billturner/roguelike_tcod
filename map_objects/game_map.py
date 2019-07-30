from random import randint
import tcod as libtcod

from components.ai import BasicMonster
from components.entity import Entity
from components.equippable import Equippable
from components.fighter import Fighter
from components.item import Item
from components.message import Message
from components.stairs import Stairs
from equipment_slots import EquipmentSlots
from functions.item import cast_confuse, cast_fireball, cast_lightning, heal
from functions.random import from_dungeon_level, random_choice_from_dict
from functions.render import RenderOrder
from map_objects.rectangle import Rect
from map_objects.tile import Tile


class GameMap:
    def __init__(self, width, height, dungeon_level=1):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

        self.dungeon_level = dungeon_level

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_room(self, room):
        # go through the tiles in the room/rectangle and make passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def initialize_tiles(self):
        # initially mark all tiles as wall/blocked
        tiles = [[Tile(True) for y in range(self.height)]
                 for x in range(self.width)]

        return tiles

    def is_blocked(self, x, y):
        return self.tiles[x][y].blocked

    def make_map(self, max_rooms, room_min_size, room_max_size, map_width,
                 map_height, player, entities, colors):
        rooms = []
        num_rooms = 0

        center_of_last_room_x = None
        center_of_last_room_y = None

        for r in range(max_rooms):
            # random width and height
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)

            # random position without going out of boundaries
            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h - 1)

            # 'rect' class makes rectangles easy
            new_room = Rect(x, y, w, h)

            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                # no intersections, it's a good room
                self.create_room(new_room)

                # center coordinates of new room
                (new_x, new_y) = new_room.center()

                center_of_last_room_x = new_x
                center_of_last_room_y = new_y

                if num_rooms == 0:
                    # this means it is first room
                    player.x = new_x
                    player.y = new_y
                else:
                    # all rooms after first
                    # connec to previous room

                    # center coords of previous room
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()

                    # flip a coin (random 0, or 1)
                    if randint(0, 1) == 1:
                        # make horizontal tunnel first
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        # make vertical tunnel first
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)

                # add monsters to the room
                self.place_entities(
                    new_room, entities, colors)

                # append new room to rooms
                rooms.append(new_room)
                num_rooms += 1

        stairs_component = Stairs(self.dungeon_level + 1)
        down_stairs = Entity(center_of_last_room_x, center_of_last_room_y, '>', libtcod.white,
                             'Stairs', render_order=RenderOrder.STAIRS, stairs=stairs_component)
        entities.append(down_stairs)

    def next_floor(self, player, message_log, constants):
        self.dungeon_level += 1
        entities = [player]

        self.tiles = self.initialize_tiles()
        self.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'],
                      constants['map_width'], constants['map_height'], player,
                      entities, constants['colors'])

        player.fighter.heal(player.fighter.max_hp // 2)

        message_log.add_message(Message(
            'You take a moment to rest, and recover your strength.', libtcod.light_violet))

        return entities

    def place_entities(self, room, entities, colors):
        # get a random number of monsters, and items
        max_monsters_per_room = from_dungeon_level(
            [[2, 1], [3, 4], [5, 6]], self.dungeon_level)
        max_items_per_room = from_dungeon_level(
            [[1, 1], [2, 4]], self.dungeon_level)

        num_monsters = randint(0, max_monsters_per_room)
        num_items = randint(0, max_items_per_room)

        monster_chances = {
            'orc': 80,
            'troll': from_dungeon_level([[15, 3], [30, 5], [60, 7]], self.dungeon_level)
        }

        item_chances = {
            'healing_potion': 35,
            'sword': from_dungeon_level([[5, 4]], self.dungeon_level),
            'shield': from_dungeon_level([[15, 8]], self.dungeon_level),
            'lightning_scroll': from_dungeon_level([[25, 4]], self.dungeon_level),
            'fireball_scroll': from_dungeon_level([[25, 6]], self.dungeon_level),
            'confusion_scroll': from_dungeon_level([[10, 2]], self.dungeon_level)
        }

        for i in range(num_monsters):
            # choose a random location in the room
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                monster_chance = random_choice_from_dict(monster_chances)

                if monster_chance == 'orc':
                    fighter_component = Fighter(
                        hp=20, defense=0, power=4, xp=35)
                    ai_component = BasicMonster()

                    monster = Entity(
                        x, y, 'o', colors.get('orc'), 'Orc',
                        blocks=True, render_order=RenderOrder.ACTOR,
                        fighter=fighter_component, ai=ai_component
                    )
                else:
                    fighter_component = Fighter(
                        hp=30, defense=2, power=8, xp=100)
                    ai_component = BasicMonster()
                    monster = Entity(
                        x, y, 'T', colors.get('troll'), 'Troll',
                        blocks=True, render_order=RenderOrder.ACTOR,
                        fighter=fighter_component, ai=ai_component
                    )

                entities.append(monster)

        for i in range(num_items):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                item_choice = random_choice_from_dict(item_chances)

                if item_choice == 'healing_potion':
                    item_component = Item(use_function=heal, amount=40)
                    item = Entity(x, y, '!', colors.get('magic_item'),
                                  'Healing Potion', render_order=RenderOrder.ITEM,
                                  item=item_component)
                elif item_choice == 'sword':
                    equippable_component = Equippable(
                        EquipmentSlots.MAIN_HAND, power_bonus=3)
                    item = Entity(x, y, '/', libtcod.sky, 'Sword',
                                  equippable=equippable_component)
                elif item_choice == 'shield':
                    equippable_component = Equippable(
                        EquipmentSlots.MAIN_HAND, defense_bonus=1)
                    item = Entity(
                        x, y, '[', libtcod.darker_orange, 'Shield', equippable=equippable_component)
                elif item_choice == 'fireball_scroll':
                    item_component = Item(use_function=cast_fireball, targeting=True, targeting_message=Message(
                        'Left-click a target tile fot the fireball, or right-click to cancel', libtcod.light_cyan), damage=25, radius=3)
                    item = Entity(x, y, '*', colors.get('magic_item'),
                                  'Fireball Scroll', render_order=RenderOrder.ITEM,
                                  item=item_component)
                elif item_choice == 'confusion_scroll':
                    item_component = Item(use_function=cast_confuse, targeting=True, targeting_message=Message(
                        'Left-click an enemy to confuse it, or right-click to cancel', libtcod.light_cyan), damage=12, radius=3)
                    item = Entity(x, y, '?', colors.get('magic_item'),
                                  'Confusion Scroll', render_order=RenderOrder.ITEM,
                                  item=item_component)
                else:
                    item_component = Item(
                        use_function=cast_lightning, damage=40, maximum_range=5)
                    item = Entity(x, y, '&', colors.get('magic_item'),
                                  'Lighning Scroll', render_order=RenderOrder.ITEM,
                                  item=item_component)

                entities.append(item)
