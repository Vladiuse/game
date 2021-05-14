import random as r

import pygame

from game_objects import Brick, Wall
from .default_game_class import Game


class Tetris(Game):
    # cube = ((0, 0), (1, 0), (1, 1), (0, 1))
    # line = ((0, 0), (0, 1),)
    # line_v = ((0, 0), (1, 0),)
    # turret_1 = ((1, 0), (1, 1), (0, 1), (1, 2))
    # turret_2 = ((0, 0), (1, 0), (2, 0), (1, 1))

    def __init__(self, controller, game_mode):
        super().__init__(controller, game_mode=game_mode)
        # self.brick = Brick(pos=(12, 0))
        self.game_objects = None
        self.wall = Wall(start_line_count=0, auto_line_add=False, direction='down', out_of_screen=True)
        self.brick = None
        self.next_brick = None
        self.next_rotation = None
        # self.add_new_brick()
        # self.game_objects = [self.brick, self.wall]
        self.player = self.brick
        self.lives = None
        # self.add_new_brick()
        self.start_game()

    def start_game(self):
        super().start_game()
        self.add_new_brick()


    def restart_game(self):
        self.game_status = True
        self.lives -= 1
        self.brick = Brick(pos=(12, 5))
        self.wall = Wall(start_line_count=0, auto_line_add=False, direction='down', out_of_screen=True)
        self.game_objects = [self.brick, self.wall]
        self.player = self.brick
        self.start_game()

    def run(self):
        if self.game_status:
            if not self.pause:
                self.player.auto_move()
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
        # shape = self.next_brick
        if not self.next_brick:
            self.next_brick = r.choice(Brick.shapes)
            self.next_rotation = r.choice(list(self.next_brick.keys()))
        self.brick = Brick(pos=(0, 5), shape=self.next_brick, rotation=self.next_rotation)
        self.player = self.brick
        self.game_objects = [self.brick, self.wall]
        # if self.array_collision(self.player, self.wall):
        #     self.game_status = False
        #     self.bomb.activate(player=self.player)
        #     self.game_objects.append(self.bomb)
        self.next_brick = r.choice(Brick.shapes)
        self.next_rotation = r.choice(list(self.next_brick.keys()))
        self.lives = {'shape':self.next_brick, 'rotation':self.next_rotation}
        self.get_small_screen_condition()
        if self.wall.get_top() <= 1:
            self.game_status = False
            self.bomb.activate(player=self.player)
            self.game_objects.append(self.bomb)
            self.lives = 0


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
        # elif key == pygame.K_UP:
        #     self.player.move_up()
        elif key == pygame.K_DOWN:
            self.player.move_down()

        elif key == pygame.K_UP:
            # print('Rotate key')
            self.brick.rotate()
            if self.array_collision(self.brick, self.wall):
                self.brick.rotate_back()
            is_out = self.player.out_screen_pos_x_in_obj()
            if is_out:
                print('Push OUT')
                if is_out > 0:
                    self.player.move_left()
                else:
                    self.player.move_right()
                print(self.player.last_direction)
                if self.array_collision(self.brick, self.wall):

                    self.brick.move_back()
                    self.brick.rotate_back()

