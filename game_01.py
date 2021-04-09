import pygame

from settings import Colors, GameSettings, GameError

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

    def __init__(self, start_point, *, game_mode):

        self.x = start_point[0]
        self.y = start_point[1]
        self.game_mode = game_mode
        self.direction = 'UP'

    def get_screen_pic(self):
        """Передает экрану (она запрашивает эту функцию)
        состояние игры"""
        pixels_screen = []
        for _ in range(0, 20):
            line = []
            for pixel in range(0, 10):
                line.append(0)
            pixels_screen.append(line)
        pixels_screen[self.y][self.x] = 1
        return pixels_screen

    def game_key_controller(self, key):
        if self.game_mode == 'step':
            self.step_mode_move(key)
        elif self.game_mode == 'traffic':
            pass
        else:
            raise GameError('неверный игровой мод')


    def traffic_mode_move(self):
        pass

    def step_mode_move(self, key):
        if key == pygame.K_LEFT:
            self.x -= 1
            if self.x == -1:
                self.x = 9
        elif key == pygame.K_RIGHT:
            self.x += 1
            if self.x == 10:
                self.x = 0

        elif key == pygame.K_UP:
            self.y -= 1
            if self.y == -1:
                self.y = 19

        elif key == pygame.K_DOWN:
            self.y += 1
            if self.y == 20:
                self.y = 0



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
