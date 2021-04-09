import pygame

class Colors:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    MY_GREEN = (20, 215, 20)
    BLUE = (0, 0, 255)
    MY_GRAY = (50, 50, 50)
    GREEN = (20, 215, 20)


class GameSettings:

    background_color = Colors.BLACK
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 800
    FPS = 30
    GAME_CAPTION = 'Tetris'
    my_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    running = True





