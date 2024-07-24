import numpy as np
import math


def calculate_energy(s, room):
    collisions = calculate_collisions(s, room)
    overlap = calculate_overlap(s, room)
    border = calculate_border(s, room)
    table_position = calculate_table_position(s, room)

    return collisions + overlap + border + table_position


def calculate_collisions(s, room):
    objects = room.create_objects()
    n = len(s)
    collisions = 0

    for i in range(n):
        for j in range(i + 1, n):
            area = max(
                0,
                min(
                    s[i][0] + objects[i].shape[0] / 2, s[j][0] + objects[j].shape[0] / 2
                )
                - max(
                    s[i][0] - objects[i].shape[0] / 2, s[j][0] - objects[j].shape[0] / 2
                ),
            ) * max(
                0,
                min(
                    s[i][1] + objects[i].shape[1] / 2, s[j][1] + objects[j].shape[1] / 2
                )
                - max(
                    s[i][1] - objects[i].shape[1] / 2, s[j][1] - objects[j].shape[1] / 2
                ),
            )
            collisions += area
    return math.sqrt(collisions)


def calculate_overlap(s, room):
    objects = room.create_objects()
    n = len(s)
    overlap = 0

    for i in range(n):
        for j in range(0, n):
            if i != j:
                area = (
                    max(
                        0,
                        min(
                            s[i][0] + objects[i].no_overlap_shape[0] / 2,
                            s[j][0] + objects[j].shape[0] / 2,
                        )
                        - max(
                            s[i][0] - objects[i].no_overlap_shape[0] / 2,
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
                            s[i][1] + objects[i].no_overlap_shape[1] / 2,
                            s[j][1] + objects[j].shape[1] / 2,
                        )
                        - max(
                            s[i][1] - objects[i].no_overlap_shape[1] / 2,
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


def calculate_border(s, room):
    objects = room.create_objects()
    n = len(s)
    border = 0

    for i in range(n):
        area = (
            max(0, -(s[i][0] - objects[i].shape[0] / 2))
            + max(0, s[i][0] + objects[i].shape[0] / 2 - room.shape[0])
        ) * objects[i].shape[1] + (
            max(0, -(s[i][1] - objects[i].shape[1] / 2))
            + max(0, s[i][1] + objects[i].shape[1] / 2 - room.shape[1])
        ) * objects[
            i
        ].shape[
            0
        ]
        border += area
    return math.sqrt(border)


def calculate_table_position(s, room):
    objects = room.create_objects()
    n = len(s)

    table_idx = [i for i in range(n) if objects[i].name == "Table"][0]
    tv_idx = [i for i in range(n) if objects[i].name == "TV"][0]
    sofa_idx = [i for i in range(n) if objects[i].name == "Canapé"][0]

    vect_sofa_tv = np.subtract(s[tv_idx], s[sofa_idx])
    vect_sofa_table = np.subtract(s[table_idx], s[sofa_idx])

    norm_vect_sofa_tv = math.sqrt(vect_sofa_tv[0] ** 2 + vect_sofa_tv[1] ** 2)
    norm_vect_sofa_table = math.sqrt(vect_sofa_table[0] ** 2 + vect_sofa_table[1] ** 2)

    tbl_score = (
        1
        - (
            (
                vect_sofa_tv[0] * vect_sofa_table[0]
                + vect_sofa_tv[1] * vect_sofa_table[1]
            )
            / (norm_vect_sofa_tv * norm_vect_sofa_table)
        )
    ) * room.shape[0]
    tbl_score += max(0, norm_vect_sofa_table - norm_vect_sofa_tv)

    return tbl_score
