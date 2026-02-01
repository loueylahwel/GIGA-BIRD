from Genome import Genome
import random

class Population:
    """Manages a population of genomes with only weight mutation"""
    def __init__(self, size):
        self.size = size
        self.generation = 0
        self.genomes = [Genome() for _ in range(size)]

    def evaluate_fitness(self, birds):
        """Assign fitness to each genome based on bird performance"""
        for i, genome in enumerate(self.genomes):
            genome.fitness = birds[i].fitness

    def evolve(self):
        """Create next generation through selection and weight mutation only"""
        # Sort by fitness
        self.genomes.sort(key=lambda g: g.fitness, reverse=True)

        # Keep elite (5%)
        next_gen = []
        elite_count = max(1, self.size // 20)
        for i in range(elite_count):
            next_gen.append(self.genomes[i].copy())

        # Add mutated clones of best (25%)
        best_clones = self.size // 4
        for _ in range(best_clones):
            clone = self.genomes[0].copy()
            clone.mutate_weights(perturb_rate=0.9, perturb_power=0.2)
            next_gen.append(clone)

        # Fill rest with mutated offspring from top parents
        while len(next_gen) < self.size:
            parent = self.tournament_select()
            child = parent.copy()
            child.mutate_weights(perturb_rate=0.9, perturb_power=0.15)
            next_gen.append(child)

        self.genomes = next_gen
        self.generation += 1

    def tournament_select(self, tournament_size=5):
        """Select a genome using tournament selection"""
        tournament = random.sample(self.genomes, min(tournament_size, len(self.genomes)))
        return max(tournament, key=lambda g: g.fitness)

    def get_best_genome(self):
        return max(self.genomes, key=lambda g: g.fitness)

    def get_average_fitness(self):
        if not self.genomes:
            return 0
        return sum(g.fitness for g in self.genomes) / len(self.genomes)