import pygame
from models import Element
WIDTH = 800
HEIGHT = 600
FPS = 30


class Player(pygame.sprite.Sprite):

    def __init__(self):
        # pygame.sprite.Sprite.__init__(self)
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

    def update(self):
        pygame.draw.ellipse(screen, GREEN,
                            (10, 50, 280, 100))
        self.rect.x += 5
        if self.rect.x > WIDTH:
            self.rect.x = 0


class Figure:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        pygame.draw.circle(screen, GREEN, (self.x, self.y), 20)
        self.x += 5
        if self.x > WIDTH:
            self.x = 0
            self.y += 50
        if self.y > HEIGHT:
            self.y = 0





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

player = Player()
all_sprites.add(player)
pygame.draw.circle(screen, BLACK, (100, 200), 30, 10)
# Цикл игры
running = True

fig = Figure(100, 100)
poligon = Element(screen=screen,start_point=(100, 100), width=20, height=80, percent=0.25)
while running:

    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
    # Обновление
    # all_sprites.update()
    # Рендеринг
    screen.fill(BLACK)
    poligon.draw()
    # all_sprites.draw(screen)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()
