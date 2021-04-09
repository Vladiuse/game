import time

import pygame

from models import Clock, Pixel, PixelScreen

WIDTH = 1200
HEIGHT = 800
FPS = 30


class Player(pygame.sprite.Sprite):

    def __init__(self):
        # pygame.sprite.Sprite.__init__(self)
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.direction = None
        self.speed = 10

    def update(self):

        pygame.draw.ellipse(screen, GREEN,
                            (10, 50, 280, 100))
        if self.rect.x < 0:
            self.rect.x = WIDTH
        if self.rect.x > WIDTH:
            self.rect.x = 0
        if self.rect.y < 0:
            self.rect.y = HEIGHT
        if self.rect.y > HEIGHT:
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


pygame.init()
pygame.mixer.init()  # для звука
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# player = Player()
# all_sprites.add(player)

# Цикл игры
running = True




def get_screen_pic(to_line, to_col):
    pixels_screen = []
    for _ in range(0, 20):
        line = []
        for pixel in range(0, 10):
            line.append(0)
        pixels_screen.append(line)
    pixels_screen[to_line][to_col] = 1
    return pixels_screen

to_show = get_screen_pic(5,8)
pixel_screen = PixelScreen(screen=screen, start_point=(250, 25), pixel_size=33, pixel_between=1.12, controller=to_show)
my_clock = Clock(screen=screen, start_time=time.time(), mili_secs=False, start_point=(650, 40), width=20)


while running:

    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        # elif event.type == pygame.KEYDOWN:
        #     print('DOWN')
        #     player.last_key(event.key)

    # Обновление

    # all_sprites.update()
    # Рендеринг
    screen.fill(BLACK)
    my_clock.show()

    # all_sprites.draw(screen)
    pixel_screen.draw()
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()
