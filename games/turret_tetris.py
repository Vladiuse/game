import time

import pygame

from game_objects import Turret, Wall, Bullet
from .default_game_class import Game


class TurretTetris(Game):
    """modes :
    build, destroy
    """
    max_bullet_count = 3
    SCORE = 1

    def __init__(self, controller, game_mode='build', game_speed=1, game_level=1):
        super().__init__(controller=controller, game_mode=game_mode,)
        self.game_speed = game_speed
        self.game_level = game_level
        self.start_time = time.time()
        self.turret = Turret((5, 18))
        self.player = self.turret
        self.bullets = []
        self.wall = Wall(direction='up',out_of_screen=True, line_add_speed=game_speed, start_line_count=2 + game_level)
        self.game_status = True
        self.game_objects = [self.turret, self.wall]
        self.score = 0
        self.start_game()

    def start_game(self):
        super().start_game()
        """Иницилизация стартового состояния игры"""

    def restart_game(self):
        self.lives -= 1
        self.start_time = time.time()
        self.turret = Turret((5, 18))
        self.bullets = []
        self.wall = Wall(direction='up',out_of_screen=True, line_add_speed=self.game_speed, start_line_count=2 + self.game_level)
        self.game_status = True
        self.game_objects = [self.turret, self.wall]
        self.start_game()

    def run(self):
        if self.game_status:
            self.check_bullet_in_screen()
            for bullet in self.bullets:
                bullet.move()
            self.collision()
            self.wall.act()
            if self.game_mode == 'build':
                self.score = self.wall.del_lines_counter
            self.render(*self.game_objects, *self.bullets)
        else:
            self.end_game()

    def create_bullet(self):
        if len(self.bullets) != TurretTetris.max_bullet_count:
            y, x = self.turret.get_position()
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
        if self.wall._get_down() == self.turret.get_position()[0]:
            self.game_status = False
            self.bomb.activate(player=self.player)
            self.game_objects.append(self.bomb)
        """Bullet - Wall collision"""
        for bullet_id, bullet in enumerate(self.bullets):
            if self.array_collision(self.wall, bullet):
                # print(id(bullet), bullet.get_obj(), bullet.number)
                y,x = bullet.get_pos()
                if self.game_mode == 'build':
                    self.wall.add_brick((y + 1, x))
                    self.score = self.wall.del_lines_counter
                else:
                    self.wall.drop_brick((y,x))
                    self.score += 1
                self.bullets.pop(bullet_id)
                # break




        # if self.bullets:
        #     for bullet_id, bullet in enumerate(self.bullets):
        #         y, x = bullet.get_pos()
        #         if (y, x) in self.wall.get_obj():
        #             if self.game_mode == 'build':
        #                 self.wall.add_brick((y + 1, x))
        #             else:
        #                 self.wall.drop_brick((y, x))
        #             self.bullets.pop(bullet_id)
        #             self.score += 1
        #         if y == - 1:
        #             if self.game_mode == 'build':
        #                 self.wall.add_brick((y + 1, x))

    def game_key_controller(self, key):
        super().game_key_controller(key=key)
        if key == pygame.K_UP:
            self.create_bullet()
        elif key == pygame.K_ESCAPE:
            self.controller.chose_game('default')
        else:
            self.turret.move(key)
