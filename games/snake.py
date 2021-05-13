import random as r
import time

import pygame

from .default_game_class import Game
from game_objects import SnakeObj, SnakeFood

def render_counter_param(n):
    counter = 0

    def render_counter(func):
        def surrogate(*args, **kwargs):
            nonlocal counter
            counter += 1
            if counter == n:
                counter = 0
                return func(*args, **kwargs)

        return surrogate

    return render_counter

class GameOver:
    blink = 10

    def __init__(self, game):
        self.game = game
        self.pause = 10
        self.flag = 1
        self.blink = 4

    def end_game(self):
        self.pause -= 1
        if self.blink == 0:
            self.game_over_param_to_default()
            self.game.restart_game()
        if self.pause == 0:
            self.pause = 10
            if self.flag == 1:
                self.blink -= 1
                self.flag *= -1
                self.game.get_null_screen()
            else:
                self.flag *= -1
                self.game.draw_snake()

    def game_over_param_to_default(self):
        self.pause = 15
        self.flag = 1
        self.blink = 4

    @render_counter_param(blink)
    def some_func(self):
        self.game_over_param_to_default()



class Snake(Game):
    """
    game_modes: traffic, step
    """

    def __init__(self, controller, game_mode='traffic'):
        super().__init__(controller=controller, game_mode=game_mode)
        # self.controller = controller
        self.direction = None
        self.last_direction = None
        self.game_condition = []
        self.snake = [[5, 17], [5, 18]]
        self.snake_food = None
        self.lives = 4
        self.start_game()
        self.game_speed = 10
        self.fps = 30
        self.speed_counter = self.fps / self.game_speed
        self.game_status = True
        self.game_over = GameOver(self)
        self.score = 0
        self.start_time = time.time()
        self.food_render = 20


    def draw_snake(self):
        for pixel in self.snake:
            y = pixel[1]
            x = pixel[0]
            self.game_condition[y][x] = 1

    def get_null_screen(self):
        self.game_condition.clear()
        line = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        while len(self.game_condition) != 20:
            self.game_condition.append(line.copy())

    def restart_game(self):
        self.start_time = time.time()
        self.snake = [[4, 17], [4, 18]]
        # self.snake = [[4, 9], [4, 10], [4, 11], [4, 12], [4, 13], [4, 14], [4, 15]]
        self.snake_food = None
        self.game_status = True
        self.game_condition = []
        self.start_game()
        self.score = 0

    def start_game(self):
        """Иницилизация стартового состояния игры"""
        super().start_game()
        line = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        while len(self.game_condition) != 20:
            self.game_condition.append(line.copy())
        self.draw_snake()
        # self.make_snake_food((2, 15))
        self.make_snake_food()

        if self.game_mode == 'traffic':
            self.direction = 'UP'
            self.last_direction = 'UP'

    def make_snake_food(self, food_coor=None):
        snake_head = self.snake[0]
        y = snake_head[1]
        x = snake_head[0]
        while [x, y] in self.snake:
            x = r.randint(0, 9)
            y = r.randint(0, 19)
        if food_coor:
            y = food_coor[1]
            x = food_coor[0]
        self.snake_food = [x, y]
        self.game_condition[y][x] = 1

    def render_food(self):
        if self.food_render == 0:
            self.food_render = 20
        self.food_render -= 1
        y = self.snake_food[1]
        x = self.snake_food[0]
        if self.food_render < 10:
            self.game_condition[y][x] = 0
        else:
            self.game_condition[y][x] = 1

    def run(self):
        """Изменение состояние игры"""
        if self.game_status:
            if self.game_mode == 'traffic':
                self.render_food()
                self.speed_counter -= 1
                if self.speed_counter <= 0:  # orig if self.speed_counter == 0:
                    self.snake_move()
                    self.speed_counter = self.fps / self.game_speed
            if self.game_mode == 'step':
                self.render_food()
                if self.direction is not None:
                    self.snake_move()
                    self.direction = None
        else:
            # self.direction = None
            self.game_over.end_game()

    def snake_move(self):
        # [y][x]
        snake_head = self.snake[0].copy()
        y = snake_head[1]
        x = snake_head[0]
        if self.direction == 'UP':
            y -= 1
        elif self.direction == 'DOWN':
            y += 1
        elif self.direction == 'LEFT':
            x -= 1
        elif self.direction == 'RIGHT':
            x += 1
        if x == -1:
            x = 9
        elif x == 10:
            x = 0
        elif y == -1:
            y = 19
        elif y == 20:
            y = 0
        new_snake_head = [x, y]
        if not new_snake_head == self.snake_food:  # не нашли ли мы еду
            if not new_snake_head in self.snake:  # не движемся ли сами в себя
                snake_end = self.snake[-1]
                # удаление хваста змеи
                self.game_condition[snake_end[1]][snake_end[0]] = 0
                self.snake.pop()
                self.last_direction = self.direction
            else:
                self.game_status = False
                print('Snake CRASH')
        else:
            # нашли еду
            self.make_snake_food()
            self.last_direction = self.direction
            self.score += 1
        # отрисовка и добовление новой головы змейки
        self.snake.insert(0, new_snake_head)
        self.game_condition[new_snake_head[1]][new_snake_head[0]] = 1
        self.last_direction = self.direction

    def get_screen_pic(self):
        """Передает экрану (он запрашивает эту функцию)
        состояние игры"""
        return self.game_condition

    def game_key_controller(self, key):
        """Меняет флаг направление движения -
        изменение на противоположное не проходит"""
        if key == pygame.K_LEFT:
            if self.last_direction != 'RIGHT':
                self.direction = 'LEFT'
        elif key == pygame.K_RIGHT:
            if self.last_direction != 'LEFT':
                self.direction = 'RIGHT'
        elif key == pygame.K_UP:
            if self.last_direction != 'DOWN':
                self.direction = 'UP'
        elif key == pygame.K_DOWN:
            if self.last_direction != 'UP':
                self.direction = 'DOWN'
        elif key == pygame.K_ESCAPE:
            self.controller.chose_game('default')



class SnakeCopy(Game):
    """game_modes: traffic, step"""

    def __init__(self, controller, game_mode='traffic'):
        super().__init__(controller=controller, game_mode=game_mode)
        self.snake = SnakeObj()
        self.player = self.snake
        self.speed_counter = self.fps / self.game_speed
        self.snake_food = SnakeFood(self.snake)
        self.game_objects = [self.snake, self.snake_food]
        self.game_over = GameOver(self)
        self.food_render = 20
        self.frame_counter = 0
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
                    self.frame_counter += 1
                    if self.frame_counter > self.speed_counter:
                        self.snake.move()
                        self.frame_counter = 0
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
        # if key == pygame.K_ESCAPE:
        #     self.controller.chose_game('default')
        # if key == pygame.K_p:
        #     self.pause_game()
        # # if key == pygame.K_x:
        # #     self.game_status = False

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
