# IMPORT MODULES
import pygame as pg

class Ball:

    def __init__(self, x: int, y: int, radius: int) -> None:
        """Defines the constructor for a Ball object"""
        self.x = x
        self.y = y
        self.radius = radius
        self.vx = -5
        self.vy = 5
        self.pos = pg.Vector2(x, y)
