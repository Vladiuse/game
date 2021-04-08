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

# class NumberElement(BaseElement):
#
#     number_code = {'0': [1, 1, 1, 0, 1, 1, 1],
#                    '1': [0, 0, 1, 0, 0, 1, 0],
#                    '2': [1, 0, 1, 1, 1, 0, 1],
#                    '3': [1, 0, 1, 1, 0, 1, 1],
#                    '4': [0, 1, 1, 1, 0, 1, 0],
#                    '5': [1, 1, 0, 1, 0, 1, 1],
#                    '6': [1, 1, 0, 1, 1, 1, 1],
#                    '7': [1, 0, 1, 0, 0, 1, 0],
#                    '8': [1, 1, 1, 1, 1, 1, 1],
#                    '9': [1, 1, 1, 1, 0, 1, 1],
#                    }
#
#     def __init__(self):



class NumberBlock(BaseElement):

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
    # off_color = MY_GRAY
    # on_color = GREEN

    def __init__(self, screen, start_point, width):
        super().__init__(screen=screen, start_point=start_point)
        # self.screen = screen
        # self.start_point = start_point
        self.width = width / 5
        self.height = self.width * 4
        self.percent = 0.25

    def draw_number_block(self, number):
        x = self.x
        y = self.y
        coof = self.width / 20
        coord_coofs = (
            (x, y),
            (x - coof * 11, y + coof * 11),
            (x + self.height - coof * 9, y + coof * 11),
            (x, y + self.height + coof * 2),
            (x - coof * 11, y + self.height + coof * 13),
            (x + self.height - coof * 9, y + self.height + coof * 13),
            (x, y + self.height * 2 + coof * 4)
        )
        colors = [NumberBlock.on_color if x == 1 else NumberBlock.off_color for x in NumberBlock.number_code[number]]
        is_horizontals = (True, False, False, True, False, False, True)
        for (x, y), horizontal, color in zip(coord_coofs, is_horizontals, colors):
            polygon_coords = self.get_polygon_coords((x, y), horizontal=horizontal)
            pygame.draw.polygon(self.screen, color, polygon_coords)

    def get_polygon_coords(self, start_point, horizontal=False):
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
        for _ in range(self.count_numbers):
            number = NumberBlock(screen=self.screen, start_point=(x, y), width=width)
            numbers.append(number)
            x += width * 1.2
            if _ == 1 or (_ == 3 and self.mili_secs is True):
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
        # self.screen = screen
        # self.x = start_point[0]
        # self.y = start_point[1]
        self.size = size

    def draw(self):
        pygame.draw.rect(self.screen, color=self.color,
                         rect=(self.x, self.y, self.size, self.size), width=0)

        new_size = self.size *0.9
        inside_x = int(self.x + self.size/20)
        inside_y = int(self.y + self.size/20)
        pygame.draw.rect(self.screen, color=BLACK,
                         rect=(inside_x, inside_y, new_size, new_size), width=0)

        center = self.size *0.7
        center_x = int(self.x + self.size*0.15)
        center_y = int(self.y + self.size*0.15)
        pygame.draw.rect(self.screen, color=self.color,
                         rect=(center_x, center_y, center, center), width=0)