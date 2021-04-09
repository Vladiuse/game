import time

import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (20, 215, 20)
BLUE = (0, 0, 255)
MY_GRAY = (50, 50, 50)


class BaseElement:
    off_color = MY_GRAY
    on_color = GREEN

    def __init__(self, screen, start_point):
        self.screen = screen
        self.start_point = start_point
        self.x = start_point[0]
        self.y = start_point[1]
        self.color = MY_GRAY

    def on(self):
        self.color = BaseElement.on_color

    def off(self):
        self.color = BaseElement.off_color

    def work(self, work):
        if work:
            return BaseElement.on_color
        return BaseElement.off_color


class NumberElement(BaseElement):

    def __init__(self, screen, start_point, width):
        super().__init__(screen=screen, start_point=start_point)
        self.width = width / 5
        self.height = self.width * 4
        self.percent = 0.25

    def get_polygon_coords(self, start_point, horizontal=False):
        """Принимает координаты и ориентацию блока,
        возвражает список с нужными координатами для отрисовки элемента"""
        percent = self.height * self.percent / 2
        polygon_coors = ([0, percent], [self.width / 2, 0], [self.width, percent],
                         [self.width, self.height - percent], [self.width / 2, self.height],
                         [0, self.height - percent])
        if horizontal:
            for point in polygon_coors:
                point[0], point[1] = point[1], point[0]

        x = start_point[0]
        y = start_point[1]
        for point in polygon_coors:
            point[0] += x
            point[1] += y
        return polygon_coors

    def draw_element(self, work, polygon_coords):
        color = self.work(work)
        pygame.draw.polygon(self.screen, color, polygon_coords)


class NumberBlock(NumberElement):
    number_code = {'0': [1, 1, 1, 0, 1, 1, 1],
                   '1': [0, 0, 1, 0, 0, 1, 0],
                   '2': [1, 0, 1, 1, 1, 0, 1],
                   '3': [1, 0, 1, 1, 0, 1, 1],
                   '4': [0, 1, 1, 1, 0, 1, 0],
                   '5': [1, 1, 0, 1, 0, 1, 1],
                   '6': [1, 1, 0, 1, 1, 1, 1],
                   '7': [1, 0, 1, 0, 0, 1, 0],
                   '8': [1, 1, 1, 1, 1, 1, 1],
                   '9': [1, 1, 1, 1, 0, 1, 1],
                   }
    is_horizontals = (True, False, False, True, False, False, True)

    def get_coofs_for_block_7(self):
        """Расчитать стартовую точку для каждого из 7 элеметнов блока"""
        coof = self.width / 20  # коофициет растояния между элементами
        coord_coofs = (
            (self.x, self.y),
            (self.x - coof * 11, self.y + coof * 11),
            (self.x + self.height - coof * 9, self.y + coof * 11),
            (self.x, self.y + self.height + coof * 2),
            (self.x - coof * 11, self.y + self.height + coof * 13),
            (self.x + self.height - coof * 9, self.y + self.height + coof * 13),
            (self.x, self.y + self.height * 2 + coof * 4)
        )
        return coord_coofs

    def draw_number_block(self, number: str):
        """принимает число на вход - отриловывает блок из 7 елеметнов с этим числом"""
        coord_coofs = self.get_coofs_for_block_7()
        works = [bool(work) for work in NumberBlock.number_code[number]]
        for start_point, horizontal, work in zip(coord_coofs, NumberBlock.is_horizontals, works):
            polygon_coords = self.get_polygon_coords(start_point, horizontal=horizontal)
            self.draw_element(work, polygon_coords)


class Clock:

    def __init__(self, screen, start_time, start_point, width, mili_secs=False):
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
            number = NumberBlock(screen=self.screen, start_point=(x, y), width=width)
            numbers.append(number)
            x += width * 1.2
            if between_number == 1 or (between_number == 3 and self.mili_secs is True):
                x += width / 4
                cpor_color = GREEN
                if int(current_time[-2]) % 2 == 0:
                    cpor_color = MY_GRAY
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


class Pixel(BaseElement):

    def __init__(self, screen, start_point, size):
        super().__init__(screen=screen, start_point=start_point)
        self.size = size

    def draw(self):
        pygame.draw.rect(self.screen, color=self.color,
                         rect=(self.x, self.y, self.size, self.size), width=0)

        new_size = self.size * 0.9
        inside_x = int(self.x + self.size / 20)
        inside_y = int(self.y + self.size / 20)
        pygame.draw.rect(self.screen, color=BLACK,
                         rect=(inside_x, inside_y, new_size, new_size), width=0)

        center = self.size * 0.7
        center_x = int(self.x + self.size * 0.15)
        center_y = int(self.y + self.size * 0.15)
        pygame.draw.rect(self.screen, color=self.color,
                         rect=(center_x, center_y, center, center), width=0)
