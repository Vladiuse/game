import time

import pygame

from .elements import Pixel, NumberBlock
from settings import GameSettings

screen = GameSettings.my_screen


class Clock:

    def __init__(self, start_time, mili_secs=False):
        self.screen = screen
        self.start_point = (700, 40)
        self.count_numbers = 4
        # self.start_time = start_time
        self.mili_secs = mili_secs
        self.width = 20

    def freeze_time(self):
        self.start_time = time.time()

    def show(self, start_time):
        width = self.width
        if self.mili_secs:
            self.count_numbers += 1
        x = self.start_point[0]
        y = self.start_point[1]
        numbers = []
        current_time = self.get_current_time(start_time)
        for between_number in range(self.count_numbers):
            number = NumberBlock(screen=self.screen, start_point=(x, y), width=width, work=0)
            numbers.append(number)
            x += width * 1.2
            if between_number == 1 or (between_number == 3 and self.mili_secs is True):
                x += width / 4
                cpor_color = GameSettings.PIXEL_ON
                if int(current_time[-2]) % 2 == 0:
                    cpor_color = GameSettings.PIXEL_OFF
                crop_coofs = [(-width / 3.5, width * 0.7), (-width / 3.5, width * 1.2)]
                for coof_x, coof_y in crop_coofs:
                    pygame.draw.circle(self.screen, color=cpor_color, center=(x + coof_x, y + coof_y),
                                       radius=width / 10)

        for elem, number in zip(numbers, current_time):
            elem.draw_number_block(number)

    def get_current_time(self, start_time):
        current = round(time.time() - start_time, 1)
        minutes = int(current / 60)
        seconds = int(current - minutes * 60)
        mili_secs = current - int(current)
        show_time = ''
        for i in [minutes, seconds]:
            i = str(i)
            if len(i) != 2:
                i = '0' + i
            show_time += i
        show_time += str(mili_secs)[-1]
        return show_time


class PixelScreen:

    def __init__(self, controller):
        self.screen = screen
        self.x = 300
        self.y = 25
        self.pixel_size = 33  # 33 default
        self.pixel_between = 1.12
        self.pixels = []
        self.controller = controller

    def fill_screen(self):
        self.pixels.clear()
        for step_y in range(0, self.pixel_size * 20, self.pixel_size):
            pixel_line = [
                Pixel(screen=self.screen, start_point=(self.x + step_x * self.pixel_between,
                                                       self.y + step_y * self.pixel_between), size=self.pixel_size,
                      work=0)
                for step_x in range(0, self.pixel_size * 10, self.pixel_size)]
            self.pixels.append(pixel_line)

    def make_picture(self):
        screen = self.controller.get_screen_pic()
        for line_id, line in enumerate(screen):
            for pixel_id, signal in enumerate(line):
                pixel = self.pixels[line_id][pixel_id]
                if signal == 1:
                    pixel.on()

    def draw(self):
        self.edging()
        self.fill_screen()
        self.make_picture()
        for line in self.pixels:
            for pixel in line:
                pixel.draw()

    def edging(self):
        x1 = 292
        y1 = 15
        x2 = 672
        y2 = 768
        corners = [((x1, y1), (x2, y1)),
                   ((x1, y1), (x1, y2)),
                   ((x1, y2), (x2, y2)),
                   ((x2, y2), (x2, y1)), ]

        for start, end in corners:
            pygame.draw.line(self.screen, color=GameSettings.PIXEL_ON, start_pos=start, end_pos=end, width=3)





class SmallScreen:

    def __init__(self, controller):
        self.screen = screen
        self.x = 700
        self.y = 320
        self.pixel_size = 33  # 33 default
        self.pixel_between = 1.12
        self.pixels = []
        self.controller = controller

    def fill_screen(self):
        self.pixels.clear()
        for step_y in range(0, self.pixel_size * 4, self.pixel_size):
            pixel_line = [
                Pixel(screen=self.screen, start_point=(self.x + step_x * self.pixel_between,
                                                       self.y + step_y * self.pixel_between), size=self.pixel_size,
                      work=0)
                for step_x in range(0, self.pixel_size * 4, self.pixel_size)]
            self.pixels.append(pixel_line)

    def make_picture(self):
        screen = self.controller.get_small_screen_pic()
        for line_id, line in enumerate(screen):
            for pixel_id, signal in enumerate(line):
                pixel = self.pixels[line_id][pixel_id]
                if signal == 1:
                    pixel.on()

    def draw(self):
        # self.edging()
        self.fill_screen()
        self.make_picture()
        for line in self.pixels:
            for pixel in line:
                pixel.draw()


class Score:

    def __init__(self, start_point, width):
        self.count_numbers = 4
        self.score = 0
        self.start_point = start_point
        self.width = width

    def show(self, numbers_code):
        x = self.start_point[0]
        y = self.start_point[1]
        for i in range(self.count_numbers):
            elem = NumberBlock(screen=screen, start_point=(x, y), width=self.width, work=0)
            x += self.width * 1.3
            elem.draw_number_block(numbers_code[i])

    def show_score(self, score):
        score = list(str(score))
        while len(score) != self.count_numbers:
            score.insert(0, 'null')
        self.show(score)


class SpeedLevel:

    def __init__(self, start_point, width):
        self.start_point = start_point
        self.width = width
        self.number_count = 2
        self.speed_level = 1

    def up_speed_level(self):
        self.speed_level += 1
        if self.speed_level == 11:
            self.speed_level = 1

    def show(self):
        self.draw_letters_on_screen()
        x = self.start_point[0]
        y = self.start_point[1]
        score = f'null-{self.speed_level}' if self.speed_level < 10 else '1-0'
        for symbol in score.split('-'):
            elem = NumberBlock(screen=screen, start_point=(x, y), width=self.width, work=0)
            x += self.width * 1.3
            elem.draw_number_block(symbol)

    def draw_letters_on_screen(self):
        x = self.start_point[0]
        y = self.start_point[1] - 50
        word = 'speed'
        for symbol in word:
            elem = NumberBlock(screen=screen, start_point=(x, y), width=self.width, work=0)
            x += self.width * 1.3
            elem.draw_number_block(symbol)



class GameLevel:

    def __init__(self, start_point, width):
        self.start_point = start_point
        self.width = width
        self.game_level = 1
        self.count_numbers = 2

    def show(self):
        self.draw_letters_on_screen()
        x = self.start_point[0]
        y = self.start_point[1]
        game_level = f'null-{self.game_level}' if self.game_level != 10 else '1-0'
        for symbol in game_level.split('-'):
            elem = NumberBlock(screen=screen, start_point=(x, y), width=self.width, work=0)
            x += self.width * 1.3
            elem.draw_number_block(symbol)

    def draw_letters_on_screen(self):
        word = 'level'
        x = self.start_point[0]
        y = self.start_point[1] - 50
        for symbol in word:
            elem = NumberBlock(screen=screen, start_point=(x, y), width=self.width, work=0)
            x += self.width * 1.3
            elem.draw_number_block(symbol)

    def up_game_level(self):
        self.game_level += 1
        if self.game_level == 11:
            self.game_level = 1



