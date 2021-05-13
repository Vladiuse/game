import pygame
from .default_game_class import Game
from game_objects import Brick, Wall
import random as r


class Tetris(Game):

    def __init__(self, controller, game_mode):
        super().__init__(controller, game_mode=game_mode)
        self.brick = Brick((10,0), Brick.cube)
        self.wall = Wall(start_line_count=0, auto_line_add=False)
        self.game_objects = [self.brick, self.wall]
        self.player = self.brick
        self.start_game()

    def start_game(self):
        super().start_game()

    def restart_game(self):
        pass

    def run(self):
        if self.game_status:
            if not self.pause:
                self.collisions()
                self.render(*self.game_objects)
        else:
            self.end_game()

    def collisions(self):
        for y,x in self.player.get_obj():
            if y == 19:
                print('DOWN')
                self.wall.add_array(self.brick.get_obj())
                self.add_new_brick()
                break  # тк возникает 2 колизии - если больше 1й точки пересечения
        if self.array_collision(self.brick, self.wall):
            self.player.move_up()
            self.wall.add_array(self.brick.get_obj())
            self.add_new_brick()


    def add_new_brick(self):
        y = r.randint(0, 3)
        x = r.randint(1,8)
        self.brick = Brick(pos=(y,x), shape=Brick.cube)
        self.player = self.brick
        self.game_objects = [self.brick, self.wall]

    def game_key_controller(self, key):
        super().game_key_controller(key=key)
        if key == pygame.K_LEFT:
            self.player.move_left()
        elif key == pygame.K_RIGHT:
            self.player.move_right()
        elif key == pygame.K_UP:
            self.player.move_up()
        elif key == pygame.K_DOWN:
            self.player.move_down()
