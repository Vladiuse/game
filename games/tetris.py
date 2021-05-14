import random as r

import pygame

from game_objects import Brick, Wall
from .default_game_class import Game


class Tetris(Game):
    cube = ((0, 0), (1, 0), (1, 1), (0, 1))
    line = ((0, 0), (0, 1),)
    line_v = ((0, 0), (1, 0),)
    turret_1 = ((1, 0), (1, 1), (0, 1), (1, 2))
    turret_2 = ((0, 0), (1, 0), (2, 0), (1, 1))

    def __init__(self, controller, game_mode):
        super().__init__(controller, game_mode=game_mode)
        self.brick = Brick(pos=(12, 0))
        self.wall = Wall(start_line_count=0, auto_line_add=False, direction='down', out_of_screen=True)
        self.game_objects = [self.brick, self.wall]
        # self.invisible_line = [(19,x) for x in range(10)]
        self.player = self.brick
        self.lives = 4
        self.start_game()

    def start_game(self):
        super().start_game()

    def restart_game(self):
        pass

    def run(self):
        if self.game_status:
            if not self.pause:
                self.collisions()
                self.wall.test_wall_check_lines()
                self.render(*self.game_objects)
        else:
            self.end_game()

    def collisions(self):
        if self.array_collision(self.brick, self.wall):
            self.player.move_up()
            self.wall.add_array(self.brick.get_obj())
            self.add_new_brick()

    def add_new_brick(self):
        # y = r.randint(0, 3)
        # x = r.randint(1,8)
        shape = r.choice(Brick.shapes)
        self.brick = Brick(pos=(5, 5), shape=shape)
        self.player = self.brick
        self.game_objects = [self.brick, self.wall]

    def game_key_controller(self, key):
        super().game_key_controller(key=key)

        if key == pygame.K_LEFT:
            self.player.move_left()
            if self.array_collision(self.brick, self.wall):
                self.player.move_right()
            if self.player.out_screen_pos_x_in_obj():
                self.player.move_right()
        elif key == pygame.K_RIGHT:
            self.player.move_right()
            if self.array_collision(self.brick, self.wall):
                self.player.move_left()
            if self.player.out_screen_pos_x_in_obj():
                self.player.move_left()
        elif key == pygame.K_UP:
            self.player.move_up()
        elif key == pygame.K_DOWN:
            self.player.move_down()
        elif key == pygame.K_r:
            print('Rotate key')
            self.brick.rotare()
