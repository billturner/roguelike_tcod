import tcod as libtcod


class Message:
    def __init__(self, text, color=libtcod.white):
        self.text = text
        self.color = color
