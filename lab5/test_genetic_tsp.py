import unittest
from genetic_tsp import *

class TestGeneticTSP(unittest.TestCase):

    def setUp(self):
        self.cities = [(0, 0), (1, 0), (1, 1), (0, 1)]
        self.population = initialize_population(10, self.cities)

    def test_initialize_population(self):
        self.assertEqual(len(self.population), 10)
        for individual in self.population:
            self.assertEqual(set(individual), set(self.cities))

    def test_evaluate_population(self):
        fitnesses = evaluate_population(self.population)
        self.assertEqual(len(fitnesses), len(self.population))
        self.assertTrue(all(f > 0 for f in fitnesses))

    def test_tournament_selection(self):
        fitnesses = evaluate_population(self.population)
        parent = tournament_selection(self.population, fitnesses)
        self.assertIn(parent, self.population)

    def test_ordered_crossover(self):
        p1 = self.population[0]
        p2 = self.population[1]
        child = ordered_crossover(p1, p2)
        self.assertEqual(set(child), set(self.cities))

    def test_mutation(self):
        original = self.population[0][:]
        mutated = mutate(original[:], mutation_rate=1.0)
        self.assertNotEqual(original, mutated)

    def test_select_next_generation(self):
        fitnesses = evaluate_population(self.population)
        offspring = create_offspring(self.population, fitnesses, 0.05)
        offspring_fitnesses = evaluate_population(offspring)
        next_gen = select_next_generation(self.population, fitnesses, offspring, offspring_fitnesses)
        self.assertEqual(len(next_gen), len(self.population))

    def test_run_algorithm(self):
        best, dist = run_genetic_algorithm(self.cities, max_iterations=10, verbose=False)
        self.assertIsInstance(best, list)
        self.assertIsInstance(dist, float)

if __name__ == '__main__':
    unittest.main()
