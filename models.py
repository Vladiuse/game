import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class Element:

    def __init__(self, screen, start_point, width):
        self.screen = screen
        self.start_point = start_point
        self.width = width
        self.height = self.width * 4
        self.percent = 0.25



    def draw(self):
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
        is_horizontals = (True, False, False, True, False, False, True)
        colors = (BLUE, WHITE, WHITE, GREEN, WHITE, WHITE, RED,)
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
