import pygame


class Object:
    def __init__(self, index, name, shape, color, no_overlap_shape):
        self.index = index
        self.name = name
        self.shape = shape
        self.color = color
        self.no_overlap_shape = no_overlap_shape

    def get_rect(self, position, screen_shape, room_shape):
        return pygame.Rect(
            (
                screen_shape[0] / 2
                - room_shape[0] / 2
                + position[0]
                - self.shape[0] / 2,
                screen_shape[1] / 2
                - room_shape[1] / 2
                + position[1]
                - self.shape[1] / 2,
            ),
            self.shape,
        )
