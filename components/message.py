import tcod


class Message:
    def __init__(self, text: str, color: tcod.Color = tcod.white):
        self.text = text
        self.color = color
