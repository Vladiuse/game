import time

import pygame

def render_counter_param(n):
    counter = 0

    def render_counter(func):
        def surrogate(*args, **kwargs):
            nonlocal counter
            counter += 1
            if counter == n:
                counter = 0
                return func(*args, **kwargs)

        return surrogate

    return render_counter


class PlayerWalk:

    def __init__(self):
        self.game_status = True
        self.game_condition = []
        self.start_game()
        self.score = 0
        self.start_time = time.time()
        self.player = Player((5, 18))
        self.bullets = []

    def get_screen_pic(self):
        """Передает экрану (он запрашивает эту функцию)
        состояние игры"""
        return self.game_condition

    def start_game(self):
        """Иницилизация стартового состояния игры"""
        line = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        while len(self.game_condition) != 20:
            self.game_condition.append(line.copy())

    def run(self):
        if self.game_status:
            for bullet in self.bullets:
                bullet.move()
            self.render_pic()

    def game_key_controller(self, key):
        if key == pygame.K_UP:
            self.create_bullet()
        else:
            self.player.move(key)

    def create_bullet(self):
        if len(self.bullets) != 3:
            y, x = self.player.get_position()
            bullet = Bullet((y - 1, x))
            self.bullets.append(bullet)

    def clear_screen(self):
        self.game_condition.clear()
        line = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        while len(self.game_condition) != 20:
            self.game_condition.append(line.copy())

    def render_pic(self):
        self.clear_screen()
        self.draw_player()
        self.draw_bullet()

    def draw_player(self):
        for y, x in self.player.get_obj():
            self.game_condition[y][x] = 1

    def draw_bullet(self):
        if self.bullets:
            for bullet_id, bullet in enumerate(self.bullets):
                y, x = bullet.get_position()
                if y != -1:
                    self.game_condition[y][x] = 1
                else:
                    self.bullets.pop(bullet_id)


class Player:

    def __init__(self, start_point):
        self.x, self.y = start_point

    def get_obj(self):
        obj = []
        elements = (self.y, self.x), (self.y + 1, self.x), (self.y + 1, self.x - 1), (self.y + 1, self.x + 1)
        for y, x in elements:
            if y in range(0, 20) and x in range(0, 10):
                obj.append([y, x])
        return obj

    def move(self, key):
        if key == pygame.K_LEFT:
            if self.x != 0:
                self.x -= 1
        elif key == pygame.K_RIGHT:
            if self.x != 9:
                self.x += 1

    def get_position(self):
        return self.y, self.x


class Bullet:

    def __init__(self, start_point, direction=None):
        self.x = start_point[1]
        self.y = start_point[0]
        self.direction = 'UP' if direction is None else direction
        self.counter = 0

    def __str__(self):
        return str(self.y) + ' - ' + str(self.x)

    @render_counter_param(1)
    def move(self):
        if self.direction == 'UP':
            self.y -= 1

    def get_position(self):
        return self.y, self.x

