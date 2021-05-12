import pygame
from .default_game_class import Game
from game_objects import Cursor, Wall

class DrawObjects(Game):

    def __init__(self, controller, game_mode=None):
        super().__init__(controller=controller, game_mode=game_mode)
        self.cursor = Cursor(pos=(0,0))
        self.wall = Wall(start_line_count=0, auto_line_add=False)
        self.game_objects = [self.cursor, self.wall]


    def start_game(self):
        super().start_game()

    def run(self):
        if self.game_status:
            self.render(*self.game_objects)
            self.blink_effect(self.cursor.obj)
        else:
            self.end_game()

    def draw(self):
        pos = self.cursor.get_pos()
        if pos not in self.wall.obj:
            self.wall.add_brick(pos)
        else:
            self.wall.drop_brick(pos)


    def game_key_controller(self, key):
        super().game_key_controller(key=key)
        if key == pygame.K_LEFT:
            self.cursor.move(direction='left')
        elif key == pygame.K_RIGHT:
            self.cursor.move(direction='right')
        elif key == pygame.K_UP:
            self.cursor.move(direction='up')
        elif key == pygame.K_DOWN:
            self.cursor.move(direction='down')
        elif key == pygame.K_d:
            self.draw()
        elif key == pygame.K_s:
            print(self.wall)



