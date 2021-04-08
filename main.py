import pygame
from models import Element, Clock, Pixel
import time
import sys
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
x = 250
y = 50
pixel_size = 30
between = 1.13
# pixel_line = [Pixel(screen=screen, start_point=(x + step * 1.1,y), size=pixel_size) for step in range(0, pixel_size * 10, pixel_size)]
pixel_group = []
for step_y in range(0, pixel_size*20, pixel_size):
    pixel_line = [Pixel(screen=screen, start_point=(x + step_x * between, y + step_y*between), size=pixel_size) for step_x in
                  range(0, pixel_size * 10, pixel_size)]
    pixel_group.append(pixel_line)

# pixel = Pixel(screen=screen, start_point=(1,1), size=200)

my_clock = Clock(screen=screen, start_time=time.time(), mili_secs=True,start_point=(900, 100), width=20)
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
    for line in pixel_group:
        for pixel in line:
            pixel.draw()


    # all_sprites.draw(screen)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()
