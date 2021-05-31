import random as r
import time

import pygame

from .default_game_class import Game
from game_objects import SnakeObj, SnakeFood


class Snake(Game):
    """game_modes: traffic, step"""

    FRAME = 30
    SCORE = 1

    def __init__(self, controller, game_mode='traffic', game_level=1, game_speed=1):
        super().__init__(controller=controller, game_mode=game_mode)
        self.snake = SnakeObj()
        self.player = self.snake
        self.__class__.FRAME = self.fps / game_speed
        print(self.__class__.FRAME)
        self.snake_food = SnakeFood(self.snake)
        self.game_objects = [self.snake, self.snake_food]
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
        self.game_objects = [self.snake, self.snake_food]
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
        if self.snake.get_pos() in self.snake.get_obj()[1:]:
            self.game_status = False
            self.bomb.activate(player=self.player)
            self.game_objects.append(self.bomb)
        # eat food
        if self.snake.get_pos() == self.snake_food.get_pos():
            self.snake_food.new_food(self.snake)
            self.snake.eat()
            self.score += 1

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
