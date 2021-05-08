import random as r
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
    max_bullet_count = 3

    def __init__(self, controller, game_mode='build'):

        self.controller = controller
        self.game_status = True
        self.__game_condition = []
        self.score = None
        self.start_time = None
        self.player = None
        self.bullets = None
        self.wall = None
        self.start_game()
        self.game_mode = game_mode

    def get_screen_pic(self):
        """Передает экрану (он запрашивает эту функцию)
        состояние игры"""
        return self.__game_condition

    def start_game(self):
        """Иницилизация стартового состояния игры"""
        line = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        while len(self.__game_condition) != 20:
            self.__game_condition.append(line.copy())
        self.score = 0
        self.start_time = time.time()
        self.player = Player((5, 18))
        self.bullets = []
        self.wall = Wall()
        self.game_status = True

    def end_game_check(self):
        if self.wall._get_top() == self.player.get_position()[0]:
            self.game_status = False

    def run(self):
        self.end_game_check()
        if self.game_status:
            for bullet in self.bullets:
                bullet.move()
            self.render_pic()
        else:
            self.start_game()

    def game_key_controller(self, key):
        if key == pygame.K_UP:
            self.create_bullet()
        elif key == pygame.K_ESCAPE:
            self.controller.chose_game('default')
        else:
            self.player.move(key)


    def create_bullet(self):
        if len(self.bullets) != PlayerWalk.max_bullet_count:
            y, x = self.player.get_position()
            bullet = Bullet((y - 1, x))
            self.bullets.append(bullet)

    def clear_screen(self):
        self.__game_condition.clear()
        line = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        while len(self.__game_condition) != 20:
            self.__game_condition.append(line.copy())

    def render_pic(self):
        self.collision()
        self.clear_screen()
        self.draw_player()
        self.draw_bullet()
        self.draw_wall()

    def draw_player(self):
        for y, x in self.player.get_obj():
            self.__game_condition[y][x] = 1

    def draw_bullet(self):
        if self.bullets:
            self.check_bullet_in_screen()
            for bullet in self.bullets:
                y, x = bullet.get_pos()
                self.__game_condition[y][x] = 1

    def check_bullet_in_screen(self):
        """Удаление пуль вышедших за экран"""
        for bullet_id, bullet in enumerate(self.bullets):
            y, x = bullet.get_pos()
            if y == -1:
                self.bullets.pop(bullet_id)

    def draw_wall(self):
        for y, x in self.wall.get_obj():
            self.__game_condition[y][x] = 1

    def collision(self):
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


class Wall:
    counter_for_new_line = 30 * 5

    def __init__(self, start_line_count=3):
        self.obj = []
        self.__init_wall(start_line_count)
        self.counter_for_new_line = Wall.counter_for_new_line

    def __init_wall(self, start_line_count):
        for y in range(start_line_count):
            self.__add_line(y)

    def __add_line(self, line_y_pos):
        y = line_y_pos
        line = []
        for x in range(10):
            pos = (y, x)
            if r.randint(0, 1):
                line.append(pos)
        if len(line) == 10:
            line.pop(r.randint(0,9))
        if line:
            self.obj.extend(line)
        else:
            self.__add_line(line_y_pos)

    def _get_top(self):
        top = 0
        for y, x in self.obj:
            if y > top:
                top = y
        return top

    def get_obj(self):
        self.auto_line_adder()
        self._check_line()
        return self.obj

    def auto_line_adder(self):
        self.counter_for_new_line -= 1
        if self.counter_for_new_line == 0:
            self.counter_for_new_line = Wall.counter_for_new_line
            self.__move_lines(line_y_pos=-1, direction=1)
            self.__add_line(line_y_pos=0)

    def drop_brick(self, brick_pos):
        self.obj.remove(brick_pos)

    def add_brick(self, brick_pos):
        self.obj.append(brick_pos)

    def _check_line(self):
        """Проверяет нет ли заполненных строк"""
        lines = set([y for y, x in self.obj])
        for line in lines:
            line_counter = 0
            for y, x in self.obj:
                if y == line:
                    line_counter += 1
            if line_counter == 10:
                self._del_line_and_down_rest(line)

    def _del_line_and_down_rest(self, line_y_pos):
        self.obj = list(filter(lambda pos: pos[0] != line_y_pos, self.obj))
        self.__move_lines(line_y_pos, direction=-1)

    def __move_lines(self, line_y_pos, direction=1):
        """смещает блоки ниже указаной"""
        new_obj = []
        for y, x in self.obj:
            if y > line_y_pos:
                new_brick = (y + direction, x)
                new_obj.append(new_brick)
            else:
                new_obj.append((y, x))
        self.obj = new_obj


class Bullet:


    def __init__(self, start_point, direction=None):
        self.x = start_point[1]
        self.y = start_point[0]
        self.direction = 'UP' if direction is None else direction
        self.counter = 0
        self.counter = 15
        self.obj = [[self.y, self.x]]


    def __str__(self):
        return f'Bullet: y:{self.y} x:{self.x}'


    # @render_counter_param(15)
    def move(self):
        if self.direction == 'UP':
            self.y -= 1

    def get_pos(self):
        return self.y, self.x

    def get_obj(self):
        return self.obj
