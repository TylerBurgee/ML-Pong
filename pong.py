# IMRORT MODULES
import pygame as pg
from player import Player
from enemy import Enemy
from ball import Ball
import random

class Window:

    def __init__(self, width: int, height: int) -> None:
        """Defines the constructor for a Window object"""
        self.width = width
        self.height = height
        self._reset_()
        pg.init()
        self.screen = pg.display.set_mode((self.width, self.height))
        self.clock = pg.time.Clock()

        self.enemy_destination = None
        self.player_pos_snapshot = 0

    def _reset_(self) -> None:
        """Resets game variables to their original states"""
        self.player = Player(20, self.height/2)
        self.enemy = Enemy(self.width-40, self.height/2)
        self.ball = Ball(self.width/2, self.height/2, 20)
        self.running = False
        self.enemy_destination = None
        self.player_pos_snapshot = 0

    def _handle_events_(self) -> None:
        """Handles user input events"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_w:
                    self.player.change_y = -10
                elif event.key == pg.K_s:
                    self.player.change_y = 10
            elif event.type == pg.KEYUP:
                self.player.change_y = 0

        self.player.pos.y += self.player.change_y
        self.ball.pos.x -= self.ball.vx
        self.ball.pos.y += self.ball.vy

        # MOVE ENEMY TO ITS DETERMINED DESTINATION
        if self.enemy_destination is None:
            self.enemy.pos.y += self.enemy.velocity
        elif self.enemy.pos.y < self.enemy_destination:
            self.enemy.pos.y += self.enemy.velocity
        elif self.enemy.pos.y > self.enemy_destination:
            self.enemy.pos.y -= self.enemy.velocity

    def _draw_(self) -> None:
        """Draws objects to the screen"""
        # BACKGROUND
        self.screen.fill("white")

        # BALL
        pg.draw.circle(self.screen, "black", self.ball.pos, self.ball.radius)

        # PLAYER
        pg.draw.rect(self.screen, "green", (self.player.pos.x, self.player.pos.y, self.player.width, self.player.height))

        # ENEMY
        pg.draw.rect(self.screen, "red", (self.enemy.pos.x, self.enemy.pos.y, self.enemy.width, self.enemy.height))

    def _detect_collisions_(self) -> None:
        """Detects object collisions"""
        # PLAYER BOUNDS
        if self.player.pos.y == 0 or self.player.pos.y == self.height - self.player.height:
            self.player.pos.y -= self.player.change_y

        # ENEMY BOUNDS
        if self.enemy.pos.y == 0 or self.enemy.pos.y == self.height - self.enemy.height:
            self.enemy.velocity = -self.enemy.velocity

        # BALL BOUNDS
        if self.ball.pos.x <= 0:
            self.running = False
        elif self.ball.pos.x >= self.width:
            # WRITE NEW ENEMY TRAINING DATA TO FILE
            self.enemy.write_data([[self.enemy.pos.y, self.player_pos_snapshot, self.ball.pos.y, 0]])
            self.running = False
        if self.ball.pos.y <= 0 or self.ball.pos.y >= self.height - self.ball.radius*2:
            self.ball.vy = -self.ball.vy

        # BALL & PLAYER
        if self.ball.pos.x == self.player.pos.x + self.player.width + self.ball.radius and self.ball.pos.y in range(
                int(self.player.pos.y), int(self.player.pos.y + self.player.height)):
            self.player_pos_snapshot = self.player.pos.y
            self.ball.vx = -self.ball.vx
            # ENEMY DECIDES WHERE TO POSITION ITSELF BASED ON PLAYER LOCATION
            self.enemy_destination = self.enemy.make_decision(self.player_pos_snapshot, self.player.height, self)
            print(self.enemy_destination)

        # BALL & ENEMY
        if self.ball.pos.x == self.enemy.pos.x - self.ball.radius and self.ball.pos.y in range(
                int(self.enemy.pos.y) - 100, int(self.enemy.pos.y + self.enemy.height)):
            self.ball.vx = -self.ball.vx
            # WRITE NEW ENEMY TRAINING DATA TO FILE
            self.enemy.write_data([[self.enemy.pos.y, self.player_pos_snapshot, self.ball.pos.y, 1]])

    def start(self) -> None:
        """Executes main program loop"""
        self.running = True
        while self.running:
            self._handle_events_()
            self._detect_collisions_()
            self._draw_()
            pg.display.update()
            self.clock.tick(60)

        # GAME WILL RESET AND RUN INFINITELY
        self._reset_()
        self.start()

if __name__ == "__main__":
    # INSTANTIATE Window OBJECT
    game = Window(960, 540)

    # EXECUTE MAIN PROGRAM LOOP
    game.start()
