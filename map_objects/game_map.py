from random import randint
import tcod as libtcod

from components.ai import BasicMonster
from components.fighter import Fighter
from components.item import Item
from components.item_functions import cast_fireball, cast_lightning, heal
from components.message import Message
from entity import Entity
from map_objects.rectangle import Rect
from map_objects.tile import Tile
from render_functions import RenderOrder


class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

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
                 map_height, player, entities, max_monsters_per_room,
                 max_items_per_room, colors):
        rooms = []
        num_rooms = 0

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
                    new_room, entities, max_monsters_per_room, max_items_per_room, colors)

                # append new room to rooms
                rooms.append(new_room)
                num_rooms += 1

    def place_entities(self, room, entities, max_monsters_per_room, max_items_per_room, colors):
        # get a random number of monsters, and items
        num_monsters = randint(0, max_monsters_per_room)
        num_items = randint(0, max_items_per_room)

        for i in range(num_monsters):
            # choose a random location in the room
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                if randint(0, 100) < 80:
                    fighter_component = Fighter(hp=10, defense=0, power=3)
                    ai_component = BasicMonster()

                    monster = Entity(
                        x, y, 'o', colors.get('orc'), 'Orc',
                        blocks=True, render_order=RenderOrder.ACTOR,
                        fighter=fighter_component, ai=ai_component
                    )
                else:
                    fighter_component = Fighter(hp=16, defense=1, power=4)
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
                item_chance = randint(0, 100)
                if item_chance < 70:
                    item_component = Item(use_function=heal, amount=4)
                    item = Entity(x, y, '!', colors.get('magic_item'),
                                  'Healing Potion', render_order=RenderOrder.ITEM,
                                  item=item_component)
                elif item_chance < 85:
                    item_component = Item(use_function=cast_fireball, targeting=True, targeting_message=Message(
                        'Left-click a target tile fot the fireball, or right-click to cancel', libtcod.light_cyan), damage=12, radius=3)
                    item = Entity(x, y, '*', colors.get('magic_item'),
                                  'Fireball Scroll', render_order=RenderOrder.ITEM,
                                  item=item_component)
                else:
                    item_component = Item(
                        use_function=cast_lightning, damage=20, maximum_range=5)
                    item = Entity(x, y, '&', colors.get('magic_item'),
                                  'Lighning Scroll', render_order=RenderOrder.ITEM,
                                  item=item_component)

                entities.append(item)
