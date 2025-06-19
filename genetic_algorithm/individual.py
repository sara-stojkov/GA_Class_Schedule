# This module contains the "Individual" class where will be the definition of an individual and functions concerning it

class Individual(object):

    def __init__(self, schedule):
        self.fitness = self.calc_fitness()
        self.schedule = schedule

    # Current idea: add points for each class that is not overlapping
    # Subject to change based on the implementation of an individual
    def calc_fitness(self):
        for event in self.schedule:
            pass

    def crossover(self, other):
        pass

    def mutations(self):
        pass
