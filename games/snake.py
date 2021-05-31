import random as r
import time

import pygame

from .default_game_class import Game
from game_objects import SnakeObj, SnakeFood, Wall


class Snake(Game):
    """game_modes: traffic, step"""

    level_2_scheme = ((2, 3), (2, 2), (3, 2), (2, 6), (2, 7),
                      (3, 7), (16, 2), (17, 2), (17, 3),
                      (17, 6), (17, 7), (16, 7), (9, 4),
                      (9, 5), (10, 5), (10, 4))
    level_3_scheme = ((2, 4), (2, 5), (3, 5), (3, 4), (9, 0),
                      (10, 0), (10, 1), (9, 1), (9, 8), (9, 9),
                      (10, 9), (10, 8), (17, 5), (16, 5), (16, 4), (17, 4))

    level_4_scheme = ((2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5),
             (2, 6), (17, 3), (17, 4), (17, 5), (17, 6), (17, 7),
             (17, 8), (17, 9), (7, 3), (7, 4), (7, 5), (7, 6),
             (7, 7), (7, 8), (7, 9), (12, 0), (12, 1), (12, 2),
             (12, 3), (12, 4), (12, 5), (12, 6))

    LEVELS = {
        '1': None,
        '2': level_2_scheme,
        '3': level_3_scheme,
        '4': level_4_scheme,
        '5': None,
        '6': None,
        '7': None,
        '8': None,
        '9': None,
        '10': None,
    }

    FRAME = 30
    SCORE = 1

    def __init__(self, controller, game_mode='traffic', game_level=1, game_speed=1):
        super().__init__(controller=controller, game_mode=game_mode)
        self.snake = SnakeObj()
        self.player = self.snake
        self.__class__.FRAME = self.fps / game_speed
        print(self.__class__.FRAME)
        self.snake_food = SnakeFood(self.snake)
        self.wall = Wall(start_line_count=0, auto_line_add=False,
                         direction='down', out_of_screen=True, wall_scheme=self.LEVELS[str(game_level)])
        self.game_objects = [self.snake, self.snake_food, self.wall]
        print(self.snake.obj)
        print(self.wall.get_obj())
        self.start_game()

    def start_game(self):
        super().start_game()
        """Иницилизация стартового состояния игры"""
        if self.game_mode == 'traffic':
            self.snake.direction = 'UP'
            self.snake.last_direction = 'UP'

    def restart_game(self):
        self.lives -= 1
        self.snake = SnakeObj()
        self.snake_food = SnakeFood(self.snake)
        self.player = self.snake
        self.game_status = True
        self.game_objects = [self.snake, self.snake_food, self.wall]

        self.start_game()

    def run(self):
        """Изменение состояние игры"""
        if self.game_status:
            if not self.pause:
                self.collision()
                if self.game_mode == 'traffic':
                    self.frame -= 1
                    if self.frame <= 0:
                        self.snake.move()
                        self.frame = self.__class__.FRAME
                if self.game_mode == 'step':
                    self.snake.move()
                    self.snake.direction = None
            self.render(*self.game_objects)
            self.blink_effect(self.snake_food.obj, [self.snake.get_pos()])
        else:
            self.end_game()

    def collision(self):
        # snake move in self
        # print(self.snake.get_pos(),self.snake.get_obj()[1:])
        if self.snake.get_pos() in self.snake.get_obj()[1:]:
            self.game_status = False
            self.bomb.activate(player=self.player)
            self.game_objects.append(self.bomb)
        # eat food
        if self.snake.get_pos() == self.snake_food.get_pos():
            self.snake_food.new_food(self.snake)
            self.snake.eat()
            self.score += 1
        # wall
        if self.array_collision(self.snake, self.wall):
            print('WALL COLISION')
            self.game_status = False
            self.bomb.activate(player=self.player)
            self.game_objects.append(self.bomb)


    def game_key_controller(self, key):
        """Меняет флаг направление движения -
        изменение на противоположное не проходит"""
        super().game_key_controller(key=key)
        if key == pygame.K_LEFT:
            if self.snake.last_direction != 'RIGHT':
                self.snake.direction = 'LEFT'
        elif key == pygame.K_RIGHT:
            if self.snake.last_direction != 'LEFT':
                self.snake.direction = 'RIGHT'
        elif key == pygame.K_UP:
            if self.snake.last_direction != 'DOWN':
                self.snake.direction = 'UP'
        elif key == pygame.K_DOWN:
            if self.snake.last_direction != 'UP':
                self.snake.direction = 'DOWN'
