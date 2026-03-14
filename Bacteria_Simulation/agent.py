import random

class Bacteria:

    def __init__(self, genotype="A"):
        self.genotype = genotype
        self.fitness = random.uniform(0.8, 1.2)
        self.energy = random.uniform(5, 10)

    def consume_resource(self, amount):
        self.energy += amount

    def mutate(self, mutation_rate):
        if random.random() < mutation_rate:
            self.genotype = self.genotype + "'"
            self.fitness *= random.uniform(0.9, 1.1)

    def reproduce(self):
        if self.energy > 10:
            self.energy /= 2
            child = Bacteria(self.genotype)
            child.fitness = self.fitness
            return child
        return None