import random
from agent import Bacteria

class Environment:

    def __init__(self, config):
        self.resource = config["initial_resource"]
        self.population = [Bacteria() for _ in range(config["initial_population"])]

        self.mutation_rate = config["mutation_rate"]
        self.antibiotic_level = config["antibiotic_level"]
        self.resource_consumption = config["resource_consumption"]

    def step(self):

        new_population = []

        for bacteria in self.population:

            # resource consumption
            if self.resource > 0:
                bacteria.consume_resource(self.resource_consumption)
                self.resource -= self.resource_consumption

            # antibiotic stress
            if random.random() < self.antibiotic_level * (1 - bacteria.fitness):
                continue

            # mutation
            bacteria.mutate(self.mutation_rate)

            # reproduction
            child = bacteria.reproduce()
            if child:
                new_population.append(child)

            new_population.append(bacteria)

        self.population = new_population