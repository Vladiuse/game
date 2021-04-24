import pygame
import time
import random as r

class GameOver:

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
                self.game.clear_screen()
            else:
                self.flag *= -1
                self.game.draw_snake()

    def game_over_param_to_default(self):
        self.pause = 15
        self.flag = 1
        self.blink = 4

class Snake:

    def __init__(self, *, game_mode='traffic', game_speed=5):

        self.game_mode = game_mode
        self.direction = None
        self.last_direction = None
        self.game_condition = []
        # self.snake = [[4, 9], [4, 10], [4, 11], [4, 12], [4, 13], [4, 14], [4, 15], [4, 16], [4, 17]]
        self.snake = [[4,9],[4,10]]
        self.snake_food = None
        self.start_game()
        self.game_speed = game_speed
        self.fps = 30
        self.speed_counter = self.fps / self.game_speed
        print(self.speed_counter)
        self.game_status = True
        self.game_over = GameOver(self)
        self.score = 0
        self.start_time = time.time()

    def draw_snake(self):
        for pixel in self.snake:
            y = pixel[1]
            x = pixel[0]
            self.game_condition[y][x] = 1

    def clear_screen(self):
        self.game_condition.clear()
        line = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        while len(self.game_condition) != 20:
            self.game_condition.append(line.copy())

    def restart_game(self):
        self.start_time = time.time()
        self.snake = [[4,9],[4,10]]
        # self.snake = [[4, 9], [4, 10], [4, 11], [4, 12], [4, 13], [4, 14], [4, 15]]
        self.snake_food = None
        self.game_status = True
        self.game_condition = []
        self.start_game()
        self.score = 0

    def start_game(self):
        """Иницилизация стартового состояния игры"""
        line = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        while len(self.game_condition) != 20:
            self.game_condition.append(line.copy())
        self.draw_snake()
        self.make_snake_food()

        if self.game_mode == 'traffic':
            self.direction = 'UP'
            self.last_direction = 'UP'

    def make_snake_food(self):
        snake_head = self.snake[0]
        y = snake_head[1]
        x = snake_head[0]
        while [x, y] in self.snake:
            x = r.randint(0, 9)
            y = r.randint(0, 19)
        self.snake_food = [x, y]
        self.game_condition[y][x] = 1

    def run(self):
        """Изменение состояние игры"""
        if self.game_status:
            if self.game_mode == 'traffic':
                self.speed_counter -= 1
                if self.speed_counter <= 0:  # orig if self.speed_counter == 0:
                    self.snake_move()
                    self.speed_counter = self.fps / self.game_speed
            if self.game_mode == 'step':
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
