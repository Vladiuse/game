import time

import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
MY_GRAY = (50, 50, 50)


class Element:
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
    off_color = MY_GRAY
    on_color = GREEN

    def __init__(self, screen, start_point, width):
        self.screen = screen
        self.start_point = start_point
        self.width = width / 5
        self.height = self.width * 4
        self.percent = 0.25

    def draw(self, number):
        x = self.start_point[0]
        y = self.start_point[1]
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
        colors = [Element.on_color if x == 1 else Element.off_color for x in Element.number_code[number]]
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


class DoubleCrop:

    def __init__(self, screen, start_point):
        self.screen = screen
        self.start_point = start_point

    def show(self, color):
        x = self.start_point[0]
        y = self.start_point[1]
        pygame.draw.circle(self.screen, color=color, center=(x, y), radius=4)


class Clock:

    def __init__(self, count_numbers, start_time):
        self.count_numbers = count_numbers
        self.start_time = start_time

    def show(self, screen, start_point, width=50):
        x = start_point[0]
        y = start_point[1]

        numbers = []
        current_time = self.get_current_time()
        for _ in range(self.count_numbers):
            number = Element(screen=screen, start_point=(x, y), width=width)
            numbers.append(number)
            x += width * 1.2
            if _ == 1 or _ == 3:
                x += width / 4
                cpor_color = GREEN
                if int(current_time[-2]) % 2 == 0:
                    cpor_color = MY_GRAY
                crop_coofs = ((-width / 3.5, width * 0.7), (-width / 3.5, width * 1.2))
                for coof_x, coof_y in crop_coofs:
                    crops = DoubleCrop(screen=screen, start_point=(x + coof_x, y + coof_y))
                    crops.show(color=cpor_color)
        for elem, number in zip(numbers, current_time):
            elem.draw(number)

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
