# IMPORT MODULES
import pygame as pg

class Paddle:

    def __init__(self, x: int, y: int) -> None:
        """Defines the constructor for a Paddle object"""
        self.x = x
        self.y = y
        self.width = 20
        self.height = 100
        self.pos = pg.Vector2(self.x, self.y)
        self.velocity = 10
        self.change_y = 0
