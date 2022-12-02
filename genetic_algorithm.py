import random

POPULATION_SIZE = 100

GENES = '''abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOP
QRSTUVWXYZ 1234567890, .-;:_!"#%&/()=?@${[]}'''

TARGET = "123456789"


class Individual():

    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.fitness = self.cal_fitness()

    @classmethod
    def mutated_genes(self):
        global GENES
        gene = random.choice(GENES)
        return gene

    @classmethod
    def create_gnome(self):

        global TARGET
        gnome_len = len(TARGET)

        # generate a random genome
        return [self.mutated_genes() for _ in range(gnome_len)]

    def mate(self, par2):
        child_chromosome = []
        for gp1, gp2 in zip(self.chromosome, par2.chromosome):
            prob = random.random()
            if prob < 0.4:
                child_chromosome.append(gp1)
            elif prob < 0.8:
                child_chromosome.append(gp2)
            else:
                child_chromosome.append(self.mutated_genes())
        return Individual(child_chromosome)

    def cal_fitness(self):
        global TARGET
        fitness = 0
        for gs, gt in zip(self.chromosome, TARGET):
            if gs != gt:
                fitness += 1
        return fitness


def main():
    global POPULATION_SIZE
    generation = 1

    found = False
    population = []
    for _ in range(POPULATION_SIZE):
        gnome = Individual.create_gnome()
        population.append(Individual(gnome))
    while not found:
        population = sorted(population, key=lambda x: x.fitness)

        if population[0].fitness <= 0:
            found = True
            break
        new_generation = []

        # Top 10% fittest as new generation
        s = int((10*POPULATION_SIZE)/100)
        new_generation.extend(population[:s])

        # 90% remaining slots of new generation is offspring of 2 parent
        # belong to 50% fittest community
        s = int((90*POPULATION_SIZE)/100)
        for _ in range(s):
            parent1 = random.choice(population[:25])
            parent2 = random.choice(population[:25])
            while (parent1 == parent2):
                parent1 = random.choice(population[:25])
                parent2 = random.choice(population[:25])
            # child = parent1.mate(parent2)
            # new_generation.append(child)
            child1 = parent1.mate(parent2)
            child2 = parent2.mate(parent1)
            if child1.fitness >= child2.fitness:
                new_generation.append(child2)
            else:
                new_generation.append(child1)

        population = new_generation
        # After this we have a new generation with "fittest" condition
        generation += 1
    return generation


if __name__ == "__main__":
    sum = 0
    for i in range(1000):
        sum += main()
    print("Averate generation to get the result is", sum / 1000)
