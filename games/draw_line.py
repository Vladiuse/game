import time

import pygame

from game_objects import Player, Wall, Bullet
from .default_game_class import Game





class PlayerWalk(Game):
    max_bullet_count = 3

    def __init__(self, controller, game_mode='build'):
        super().__init__(controller=controller, game_mode=game_mode)
        self.player = None
        self.bullets = None
        self.wall = None
        self.start_game()

    def start_game(self):
        super().start_game()
        """Иницилизация стартового состояния игры"""
        self.get_null_screen()
        self.score = 0
        self.start_time = time.time()
        self.player = Player((5, 18))
        self.bullets = []
        self.wall = Wall()
        self.game_status = True
        self.game_objects = [self.player, self.wall]

    def restart_game(self):
        self.get_null_screen()
        self.lives -= 1
        self.score = 0
        self.start_time = time.time()
        self.player = Player((5, 18))
        self.bullets = []
        self.wall = Wall()
        self.game_status = True
        self.game_objects = [self.player, self.wall]

    # def end_game_check(self):
    #     if self.wall._get_top() == self.player.get_position()[0]:
    #         self.game_status = False

    def run(self):
        # self.end_game_check()
        if self.game_status:
            for bullet in self.bullets:
                bullet.move()
            self.collision()
            self.check_bullet_in_screen()
            self.render(*self.game_objects, *self.bullets)
        else:
            self.end_game()
            # self.start_game()

    def create_bullet(self):
        if len(self.bullets) != PlayerWalk.max_bullet_count:
            y, x = self.player.get_position()
            bullet = Bullet((y - 1, x))
            self.bullets.append(bullet)

    def check_bullet_in_screen(self):
        """Удаление пуль вышедших за экран"""
        if self.bullets:
            for bullet_id, bullet in enumerate(self.bullets):
                y, x = bullet.get_pos()
                if y == -1:
                    self.bullets.pop(bullet_id)

    def collision(self):
        if self.wall._get_top() == self.player.get_position()[0]:
            self.game_status = False
            self.bomb.activate(player=self.player)
            self.game_objects.append(self.bomb)

        """Bullet - Wall collision"""
        if self.bullets:
            for bullet_id, bullet in enumerate(self.bullets):
                y, x = bullet.get_pos()
                if (y, x) in self.wall.get_obj():
                    if self.game_mode == 'build':
                        self.wall.add_brick((y + 1, x))
                    else:
                        self.wall.drop_brick((y, x))
                    self.bullets.pop(bullet_id)
                    self.score += 1
                if y == - 1:
                    if self.game_mode == 'build':
                        self.wall.add_brick((y + 1, x))

    def game_key_controller(self, key):
        super().game_key_controller(key=key)
        if key == pygame.K_UP:
            self.create_bullet()
        elif key == pygame.K_ESCAPE:
            self.controller.chose_game('default')
        else:
            self.player.move(key)
