import random as r

import pygame

from settings import Colors, GameSettings

screen = GameSettings.my_screen


class GameController:
    """Отслеживает нажимаемые клаиши
     - передает их в игру"""

    def __init__(self, game):
        self.game = game

    def run(self):
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                GameSettings.running = False
            elif event.type == pygame.KEYDOWN:
                self.game.game_key_controller(event.key)


class GameOver:

    def __init__(self, game):
        self.game = game
        self.pause = 15
        self.flag = 1
        self.blink = 4

    def end_game(self):
        self.pause -= 1
        if self.blink == 0:
            self.game_over_param_to_default()
            self.game.restart_game()
        if self.pause == 0:
            self.pause = 15
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


class PixelWalk:

    def __init__(self, *, game_mode):

        self.game_mode = game_mode
        self.direction = None
        self.last_direction = None
        self.game_condition = []
        self.snake = [[4, 9], [4, 10], [4, 11], [4, 12], [4, 13], [4, 14], [4, 15]]
        # self.snake = [[4,9],[4,10]]
        self.snake_food = None
        self.start_game()
        self.game_speed = 3
        self.fps = 30
        self.speed_counter = self.fps / self.game_speed
        self.game_status = True
        self.game_over = GameOver(game=self)

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
        self.snake = [[4, 9], [4, 10], [4, 11], [4, 12], [4, 13], [4, 14], [4, 15]]
        self.snake_food = None
        self.game_status = True
        self.game_condition = []
        self.start_game()

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
                if self.speed_counter == 0:
                    self.snake_move()
                    self.speed_counter = self.fps / self.game_speed
            if self.game_mode == 'step':
                if self.direction is not None:
                    self.snake_move()
                    self.direction = None
        else:
            self.direction = None
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
        if x == 10:
            x = 0
        if y == -1:
            y = 19
        if y == 20:
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
            self.make_snake_food()
            self.last_direction = self.direction
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


class Player(pygame.sprite.Sprite):

    def __init__(self):
        # pygame.sprite.Sprite.__init__(self)
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(Colors.GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (800, 500)
        self.direction = None
        self.speed = 10

    def update(self):

        if self.rect.x < 0:
            self.rect.x = GameSettings.SCREEN_WIDTH
        if self.rect.x > GameSettings.SCREEN_WIDTH:
            self.rect.x = 0
        if self.rect.y < 0:
            self.rect.y = GameSettings.SCREEN_HEIGHT
        if self.rect.y > GameSettings.SCREEN_HEIGHT:
            self.rect.y = 0
        if self.direction is None:
            pass
        if self.direction == 'LEFT':
            self.rect.x -= self.speed
        if self.direction == 'RIGHT':
            self.rect.x += self.speed
        if self.direction == 'UP':
            self.rect.y -= self.speed
        if self.direction == 'DOWN':
            self.rect.y += self.speed

    def last_key(self, key):
        if key == pygame.K_LEFT:
            self.direction = 'LEFT'
        if key == pygame.K_RIGHT:
            self.direction = 'RIGHT'
        if key == pygame.K_UP:
            self.direction = 'UP'
        if key == pygame.K_DOWN:
            self.direction = 'DOWN'
