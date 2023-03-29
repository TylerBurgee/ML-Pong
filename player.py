# IMPORT MODULES
from paddle import Paddle

class Player(Paddle):

    def __init__(self, x: int, y: int) -> None:
        """Defines the constructor for a Player object"""
        super().__init__(x, y)
