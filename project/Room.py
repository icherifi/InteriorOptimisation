import numpy as np
from Object import Object


class Room:
    def __init__(self, shape):
        self.shape = shape

    def create_objects(self):
        return [
            Object(0, "TV", (290, 40), "black", (290, 40)),
            Object(1, "Canapé", (270, 90), "blue", (270, 90)),
            Object(2, "Fauteuil1", (95, 75), "red", (115, 90)),
            Object(3, "Fauteuil2", (95, 75), "red", (115, 90)),
            Object(4, "Table", (115, 90), "yellow", (120, 95)),
            Object(5, "Plante", (105, 100), "green", (135, 120)),
        ]
