import random
import math
from EnergyCalculations import EnergyCalculations
from Room import Room
import numpy as np


class SimulatedAnnealing:
    def __init__(self, room, objects, kmax=400, T0=2000, l=0.97):
        # TODO: Add callables for energy function
        self.room = room
        self.objects = objects
        self.kmax = kmax
        self.T0 = T0
        self.l = l
        self.steps = 0

    def P(self, delta_E, T):
        return math.exp(-delta_E / T)

    def run(self):
        room = self.room
        room.add_objects(self.objects)
        s = room.state
        e = EnergyCalculations(s, room.shape, room.objects).calculate()
        m = e
        k = 0
        T = self.T0

        while k < self.kmax and e > 4:
            for _ in range(150):
                sp = self.random_neighbour(s, p=1)
                ep = EnergyCalculations(sp, room.shape, room.objects).calculate()
                if ep < e or random.random() < self.P(ep - e, T):
                    s, e = sp, ep
                if e < m:
                    g, m = s, e
            k += 1
            T *= self.l
        self.steps = k
        room.state = g
        print("Details :", EnergyCalculations(g, room.shape, room.objects).summary())
        return room, m

    def random_neighbour(self, state, p=1):

        newState = state[:]
        randomIdx = random.randrange(0, len(state))
        randomVect = random.choice([(0, p), (p, 0), (0, -p), (-p, 0)])
        newState[randomIdx] = np.add(state[randomIdx], randomVect)
        return newState
