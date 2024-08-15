import random
from typing import List
import numpy as np
import math
from Room import Room


class EnergyCalculations:

    def __init__(
        self, state: List[np.ndarray], roomDimensions: np.ndarray, objects: List
    ):
        self.roomDim = roomDimensions
        self.s = state
        self.objects = objects

    def calculate(self):
        collisions = self.calculate_collisions()
        overlap = self.calculate_overlap()
        border = self.calculate_border()
        table_position = self.calculate_table_position()
        by_wall = self.calculate_placement_wall()
        return collisions + overlap + border + table_position + by_wall

    def summary(self):
        collisions = self.calculate_collisions()
        overlap = self.calculate_overlap()
        border = self.calculate_border()
        table_position = self.calculate_table_position()
        by_wall = self.calculate_placement_wall()
        return [collisions, overlap, border, table_position, by_wall]

    def calculate_collisions(self):
        s = self.s
        n = len(s)
        collisions = 0

        for i in range(n):
            for j in range(i + 1, n):
                area = max(
                    0,
                    min(
                        s[i][0] + self.objects[i].shape[0] / 2,
                        s[j][0] + self.objects[j].shape[0] / 2,
                    )
                    - max(
                        s[i][0] - self.objects[i].shape[0] / 2,
                        s[j][0] - self.objects[j].shape[0] / 2,
                    ),
                ) * max(
                    0,
                    min(
                        s[i][1] + self.objects[i].shape[1] / 2,
                        s[j][1] + self.objects[j].shape[1] / 2,
                    )
                    - max(
                        s[i][1] - self.objects[i].shape[1] / 2,
                        s[j][1] - self.objects[j].shape[1] / 2,
                    ),
                )
                collisions += area
        return math.sqrt(collisions)

    def calculate_overlap(self):
        s = self.s
        objects = self.objects
        n = len(s)
        overlap = 0

        for i in range(n):
            for j in range(0, n):
                if i != j:
                    area = (
                        max(
                            0,
                            min(
                                s[i][0] + objects[i].virtual_shape[0] / 2,
                                s[j][0] + objects[j].shape[0] / 2,
                            )
                            - max(
                                s[i][0] - objects[i].virtual_shape[0] / 2,
                                s[j][0] - objects[j].shape[0] / 2,
                            ),
                        )
                        - max(
                            0,
                            min(
                                s[i][0] + objects[i].shape[0] / 2,
                                s[j][0] + objects[j].shape[0] / 2,
                            )
                            - max(
                                s[i][0] - objects[i].shape[0] / 2,
                                s[j][0] - objects[j].shape[0] / 2,
                            ),
                        )
                    ) * (
                        max(
                            0,
                            min(
                                s[i][1] + objects[i].virtual_shape[1] / 2,
                                s[j][1] + objects[j].shape[1] / 2,
                            )
                            - max(
                                s[i][1] - objects[i].virtual_shape[1] / 2,
                                s[j][1] - objects[j].shape[1] / 2,
                            ),
                        )
                        - max(
                            0,
                            min(
                                s[i][1] + objects[i].shape[1] / 2,
                                s[j][1] + objects[j].shape[1] / 2,
                            )
                            - max(
                                s[i][1] - objects[i].shape[1] / 2,
                                s[j][1] - objects[j].shape[1] / 2,
                            ),
                        )
                    )
                    overlap += area
        return math.sqrt(overlap)

    def calculate_border(self):
        objects = self.objects
        roomDim = self.roomDim
        s = self.s
        n = len(s)
        border = 0

        for i in range(n):
            area = (
                max(0, -(s[i][0] - objects[i].shape[0] / 2) - roomDim[0] / 2)
                + max(0, s[i][0] + objects[i].shape[0] / 2 - roomDim[0] / 2)
            ) * objects[i].shape[1] + (
                max(0, -(s[i][1] - objects[i].shape[1] / 2) - roomDim[1] / 2)
                + max(0, s[i][1] + objects[i].shape[1] / 2 - roomDim[1] / 2)
            ) * objects[
                i
            ].shape[
                0
            ]
            border += area
        return math.sqrt(border)

    def calculate_table_position(self, oritentation=(0, 1)):
        objects = self.objects
        s = self.s
        roomDim = self.roomDim
        n = len(s)

        table_idx = [i for i in range(n) if objects[i].name == "Table"][0]
        tv_idx = [i for i in range(n) if objects[i].name == "TV"][0]
        sofa_idx = [i for i in range(n) if objects[i].name == "Canapé"][0]

        vect_sofa_tv = np.subtract(s[tv_idx], s[sofa_idx])
        vect_sofa_table = np.subtract(s[table_idx], s[sofa_idx])

        norm_vect_sofa_tv = math.sqrt(vect_sofa_tv[0] ** 2 + vect_sofa_tv[1] ** 2)
        norm_vect_sofa_table = math.sqrt(
            vect_sofa_table[0] ** 2 + vect_sofa_table[1] ** 2
        )

        tbl_score = (
            1
            - (
                np.dot(vect_sofa_tv, vect_sofa_table)
                / (norm_vect_sofa_tv * norm_vect_sofa_table)
            )
        ) * roomDim[0]
        tbl_score += max(0, norm_vect_sofa_table - norm_vect_sofa_tv)
        # tbl_score += 1 - np.dot(vect_sofa_tv, oritentation) / norm_vect_sofa_tv
        # tbl_score += 1 - np.dot(vect_sofa_table, oritentation) / norm_vect_sofa_table

        return tbl_score

    def calculate_placement_wall(self):
        """_summary_
        Simple version of this function : the long part of the object should be placed along the wall. The penalty is the distance between the object and the wall.
        Returns:
            _type_: _description_
        """
        objects = self.objects
        roomDim = self.roomDim
        s = self.s
        n = len(s)
        placement_score = 0
        nb_by_wall = 0
        barycenter = np.mean(s, axis=0)
        for i in range(n):
            obj = objects[i]
            if obj.by_wall == "wall":
                nb_by_wall += 1
                isHorizontal = 1 if obj.shape[0] > obj.shape[1] else 0
                if s[i][isHorizontal] > 0:
                    placement_score += max(
                        0,
                        roomDim[isHorizontal] / 2
                        - s[i][isHorizontal]
                        - obj.shape[isHorizontal] / 2,
                    )
                else:
                    placement_score += max(
                        0,
                        roomDim[isHorizontal] / 2
                        + s[i][isHorizontal]
                        - obj.shape[isHorizontal] / 2,
                    )

        return placement_score * (nb_by_wall / len(s))
