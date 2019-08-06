from random import randint
from typing import Dict, List


def from_dungeon_level(table: List, dungeon_level: int) -> int:
    for (value, level) in reversed(table):
        if dungeon_level >= level:
            return value

    return 0


# TODO: should this return 0 by default?
def random_choice_index(chances: List) -> int:
    random_chance = randint(1, sum(chances))

    running_sum = 0
    choice = 0
    for w in chances:
        running_sum += w

        if random_chance <= running_sum:
            return choice
        choice += 1

    return 0


def random_choice_from_dict(choice_dict: Dict) -> str:
    choices = list(choice_dict.keys())
    chances = list(choice_dict.values())

    return choices[random_choice_index(chances)]
