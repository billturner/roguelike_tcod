class Tile:
    """
    A tile on a map. May or not be blocked, and may or
    may not be blocking sight.
    """

    def __init__(self, blocked: bool, block_sight: bool = None) -> None:
        self.blocked = blocked

        # by default, if tile is blocked, it blocks sight
        if block_sight is None:
            block_sight = blocked

        self.block_sight = block_sight

        self.explored: bool = False
