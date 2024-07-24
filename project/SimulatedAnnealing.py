import random
import math
from Utils import random_state, random_neighbour
from EnergyCalculations import calculate_energy


class SimulatedAnnealing:
    def __init__(self, room, kmax=400, T0=2000, l=0.97):
        self.room = room
        self.kmax = kmax
        self.T0 = T0
        self.l = l
        self.steps = 0

    def P(self, delta_E, T):
        return math.exp(-delta_E / T)

    def run(self):
        s = random_state(self.room)
        e = calculate_energy(s, self.room)
        g, m = s, e
        k = 0
        T = self.T0

        while k < self.kmax and e > 4:
            for _ in range(150):
                sp = random_neighbour(s, self.room)
                ep = calculate_energy(sp, self.room)
                if ep < e or random.random() < self.P(ep - e, T):
                    s, e = sp, ep
                if e < m:
                    g, m = s, e
            k += 1
            T *= self.l
        self.steps = k
        return g, m
