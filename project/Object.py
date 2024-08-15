from typing import List
import pygame
import numpy as np
import random
from enum import Enum


class Relation(Enum):
    AROUND = 1
    OPPOSITE = 2
    CENTER = 3
    SIDE = 4


class Object:
    def __init__(self, index, name, shape, color, virtual_shape, by_wall=False):
        self.index = index
        self.name = name
        self.shape = shape
        self.color = color
        self.virtual_shape = virtual_shape
        self.by_wall = by_wall  # True or False
        self.place = None
        self.position = None
        self.orientation = None

    def get_rect(self, position, screen_shape, room_shape):
        return pygame.Rect(
            (
                (position[0] + screen_shape[0] / 2 - self.shape[0] / 2),
                (position[1] + screen_shape[1] / 2 - self.shape[1] / 2),
            ),
            self.shape,
        )


class Parent(Object):
    def __init__(self, index, name, shape, color, virtual_shape):
        super().__init__(index, name, shape, color, virtual_shape)
        self.childs: List[Object] = []
        self.relation: Relation = None

    def add_object(self, obj: Object):
        self.childs.append(obj)
