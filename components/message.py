import tcod as libtcod


class Message:
    def __init__(self, text: str, color: libtcod.Color = libtcod.white):
        self.text = text
        self.color = color
