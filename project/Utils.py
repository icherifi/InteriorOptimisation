import random
import numpy as np


def random_state(room):
    state = [None] * len(room.create_objects())
    for obj in room.create_objects():
        state[obj.index] = np.array(
            [
                random.randint(obj.shape[0] // 2, room.shape[0] - obj.shape[0] // 2),
                random.randint(
                    obj.shape[1] // 2, room.shape[1] // 2 - obj.shape[1] // 2
                ),
            ]
        )
    return state


def random_neighbour(state, room):
    newState = state[:]
    randomIdx = random.randrange(0, len(room.create_objects()))
    randomVect = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
    newState[randomIdx] = np.add(state[randomIdx], randomVect)
    return newState
