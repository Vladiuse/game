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


class PixelWalk:

    def __init__(self, *, game_mode):

        # self.x = 4
        # self.y = 9
        self.game_mode = game_mode
        self.direction = None
        self.game_condition = []
        self.snake = [[4,9], [4,10]]
        self.start_game()
        self.game_speed = 6
        self.fps = 30
        self.speed_counter = self.fps / self.game_speed


    def draw_snake(self):
        for pixel in self.snake:
            y = pixel[1]
            x = pixel[0]
            self.game_condition[y][x] = 1

    def start_game(self):
        """Иницилизация стартового состояния игры"""
        line = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        while len(self.game_condition) != 20:
            self.game_condition.append(line.copy())
        # self.game_condition[self.y][self.x] = 1
        self.draw_snake()

        if self.game_mode == 'traffic':
            self.direction = 'UP'

    def run(self):
        """Изменение состояние игры"""
        if self.game_mode == 'traffic':
            self.speed_counter -= 1
            if self.speed_counter == 0:
                self.snake_move()
                self.speed_counter = self.fps / self.game_speed
        if self.game_mode == 'step':
            if self.direction is not None:
                self.snake_move()
                self.direction = None

        self.make_new_screen()

    def snake_move(self):
        #[y][x]
        snake_head = self.snake[0].copy()
        y = snake_head[1]
        x = snake_head[0]
        if self.direction == 'UP':
            print('y UP')
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
        new_snake_head = [x,y]
        # print(f'new snake head is {new_snake_head}')
        snake_end = self.snake[-1]
        # удаление хваста змеи
        self.game_condition[snake_end[1]][snake_end[0]] = 0
        self.snake.pop()
        self.snake.insert(0, new_snake_head)
        self.game_condition[new_snake_head[1]][new_snake_head[0]] = 1

    def get_screen_pic(self):
        """Передает экрану (он запрашивает эту функцию)
        состояние игры"""
        return self.game_condition

    def game_key_controller(self, key):
        """Меняет флаг направление движения"""
        if key == pygame.K_LEFT:
            self.direction = 'LEFT'
        elif key == pygame.K_RIGHT:
            self.direction = 'RIGHT'
        elif key == pygame.K_UP:
            self.direction = 'UP'
        elif key == pygame.K_DOWN:
            self.direction = 'DOWN'
        print(self.direction)

    def make_new_screen(self):
        """Проверка выхода за границы игрового поля и
        формирования масива для экрана"""
        # self.draw_snake()
        pass
        # if self.x == -1:
        #     self.x = 9
        # if self.x == 10:
        #     self.x = 0
        # if self.y == -1:
        #     self.y = 19
        # if self.y == 20:
        #     self.y = 0
        # self.game_condition.clear()
        # for _ in range(0, 20):
        #     line = []
        #     for pixel in range(0, 10):
        #         line.append(0)
        #     self.game_condition.append(line)
        # self.game_condition[self.y][self.x] = 1


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
