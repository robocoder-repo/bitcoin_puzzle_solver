import random
from typing import List, Tuple
from bitcoin_utils import private_key_to_address

class GeneticSolver:
    def __init__(self, target_addresses: List[str], population_size: int = 100, mutation_rate: float = 0.01):
        self.target_addresses = target_addresses
        self.population_size = population_size
        self.mutation_rate = mutation_rate

    def generate_individual(self) -> str:
        return ''.join(random.choice('0123456789abcdef') for _ in range(64))

    def fitness(self, individual: str) -> int:
        address = private_key_to_address(individual)
        return 1 if address in self.target_addresses else 0

    def crossover(self, parent1: str, parent2: str) -> str:
        split = random.randint(0, 63)
        return parent1[:split] + parent2[split:]

    def mutate(self, individual: str) -> str:
        return ''.join(c if random.random() > self.mutation_rate else random.choice('0123456789abcdef') for c in individual)

    def evolve(self, generations: int) -> Tuple[str, str]:
        population = [self.generate_individual() for _ in range(self.population_size)]

        for _ in range(generations):
            population = sorted(population, key=self.fitness, reverse=True)
            
            if self.fitness(population[0]) == 1:
                return population[0], private_key_to_address(population[0])

            new_population = population[:2]  # Keep the two best individuals

            while len(new_population) < self.population_size:
                parent1, parent2 = random.sample(population[:50], 2)
                child = self.crossover(parent1, parent2)
                child = self.mutate(child)
                new_population.append(child)

            population = new_population

        return None, None
