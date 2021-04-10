import pygame
import time
from elements import Pixel, NumberBlock
from settings import Colors, GameSettings
screen = GameSettings.my_screen


class Clock:

    def __init__(self,start_time, start_point, width, mili_secs=False):
        self.screen = screen
        self.start_point = start_point
        self.count_numbers = 4
        self.start_time = start_time
        self.mili_secs = mili_secs
        self.width = width

    def show(self):
        width = self.width
        if self.mili_secs:
            self.count_numbers += 1
        x = self.start_point[0]
        y = self.start_point[1]
        numbers = []
        current_time = self.get_current_time()
        for between_number in range(self.count_numbers):
            number = NumberBlock(screen=self.screen, start_point=(x, y), width=width, work=0)
            numbers.append(number)
            x += width * 1.2
            if between_number == 1 or (between_number == 3 and self.mili_secs is True):
                x += width / 4
                cpor_color = Colors.GREEN
                if int(current_time[-2]) % 2 == 0:
                    cpor_color = Colors.MY_GRAY
                crop_coofs = [(-width / 3.5, width * 0.7), (-width / 3.5, width * 1.2)]
                for coof_x, coof_y in crop_coofs:
                    pygame.draw.circle(self.screen, color=cpor_color, center=(x + coof_x, y + coof_y),
                                       radius=width / 10)

        for elem, number in zip(numbers, current_time):
            elem.draw_number_block(number)

    def get_current_time(self):
        current = round(time.time() - self.start_time, 1)
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

    def __init__(self, game):
        self.screen = screen
        self.x = 250
        self.y = 25
        self.pixel_size = 33
        self.pixel_between = 1.12
        self.pixels = []
        self.game = game

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
        screen = self.game.get_screen_pic()
        for line_id, line in enumerate(screen):
            for pixel_id, signal in enumerate(line):
                pixel = self.pixels[line_id][pixel_id]
                if signal == 1:
                    pixel.on()

    def draw(self):
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
            print('we in show_score', i, numbers_code)
            elem = NumberBlock(screen=screen,start_point=(x,y), width=self.width, work=0)
            x += self.width * 1.3
            elem.draw_number_block(numbers_code[i])


    def get_score(self, score):
        pass

    def show_score(self, score):
        score = list(str(score))
        while len(score) != self.count_numbers:
            score.insert(0, 'null')
        self.show(score)

