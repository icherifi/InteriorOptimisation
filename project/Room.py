import random
import numpy as np
from Object import Object


class Room:
    def __init__(self, shape):
        self.shape = shape
        self.objects = None
        self.state = None

    def add_objects(self, objects):
        for obj in objects:
            # (0,0) is the center of the room
            obj.position = np.array(
                [
                    random.randint(
                        (-self.shape[0] // 2 + obj.shape[0] // 2),
                        (self.shape[0] // 2 - obj.shape[0] // 2),
                    ),
                    random.randint(
                        (-self.shape[1] // 2 + obj.shape[1] // 2),
                        (self.shape[1] // 2 - obj.shape[1] // 2),
                    ),
                ]
            )
            obj.orientation = np.random.randint(-1, 1)
        self.objects = objects
        self.state = [obj.position for obj in objects]
