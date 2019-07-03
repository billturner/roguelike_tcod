class Entity:
    """Generic object to represent players, monsters, items, etc"""

    def __init__(self, x, y, char, color, name, blocks=False):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks

    def move(self, dx, dy):
        # move entity a given amount
        self.x += dx
        self.y += dy
