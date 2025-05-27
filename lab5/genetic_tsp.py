import random
import math
import itertools

# 1: ініціалізація популяції 
def initialize_population(num_individuals, cities):
    return [random.sample(cities, len(cities)) for _ in range(num_individuals)]

# 2: оцінка придатності (Fitness)
def calculate_total_distance(path):
    return sum(math.dist(path[i], path[(i + 1) % len(path)]) for i in range(len(path)))

def evaluate_population(population):
    return [calculate_total_distance(individual) for individual in population]

# 3: вибір батьків
def tournament_selection(population, fitnesses, k=3):
    selected = random.sample(list(zip(population, fitnesses)), k)
    selected.sort(key=lambda x: x[1])
    return selected[0][0]

# 4: кросовер і мутація 
def ordered_crossover(parent1, parent2):
    start, end = sorted(random.sample(range(len(parent1)), 2))
    child = [None]*len(parent1)
    child[start:end] = parent1[start:end]
    ptr = end
    for city in parent2:
        if city not in child:
            if ptr >= len(parent1):
                ptr = 0
            child[ptr] = city
            ptr += 1
    return child

def mutate(individual, mutation_rate=0.05):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            j = random.randint(0, len(individual) - 1)
            individual[i], individual[j] = individual[j], individual[i]
    return individual

def create_offspring(population, fitnesses, mutation_rate):
    offspring = []
    for _ in range(len(population)):
        parent1 = tournament_selection(population, fitnesses)
        parent2 = tournament_selection(population, fitnesses)
        child = ordered_crossover(parent1, parent2)
        mutated_child = mutate(child, mutation_rate)
        offspring.append(mutated_child)
    return offspring

# 5: оцінка нової популяції
# Використовується evaluate_population()

# 6: вибір нової популяції (елітність) 
def select_next_generation(population, fitnesses, offspring, offspring_fitnesses, elite_size=1):
    combined = list(zip(population, fitnesses)) + list(zip(offspring, offspring_fitnesses))
    combined.sort(key=lambda x: x[1])
    return [individual for individual, _ in combined[:len(population)]]

# 7: умова зупинки
def stopping_condition(iteration, max_iterations, stable_counter, stable_limit):
    return iteration >= max_iterations or stable_counter >= stable_limit

# 8: вивід результатів
def get_best_solution(population, fitnesses):
    min_index = fitnesses.index(min(fitnesses))
    return population[min_index], fitnesses[min_index]

# основний алгоритм 
def run_genetic_algorithm(
    cities,
    num_individuals=50,
    max_iterations=500,
    mutation_rate=0.05,
    elite_size=1,
    stable_limit=50,
    verbose=True
):
    population = initialize_population(num_individuals, cities)
    fitnesses = evaluate_population(population)

    best_distance = min(fitnesses)
    stable_counter = 0

    for iteration in range(max_iterations):
        offspring = create_offspring(population, fitnesses, mutation_rate)
        offspring_fitnesses = evaluate_population(offspring)

        new_population = select_next_generation(
            population, fitnesses, offspring, offspring_fitnesses, elite_size
        )
        new_fitnesses = evaluate_population(new_population)

        current_best = min(new_fitnesses)
        if current_best < best_distance:
            best_distance = current_best
            stable_counter = 0
        else:
            stable_counter += 1

        population = new_population
        fitnesses = new_fitnesses

        if verbose:
            print(f"Iteration {iteration + 1}: Best Distance = {best_distance:.2f}")

        if stopping_condition(iteration + 1, max_iterations, stable_counter, stable_limit):
            break

    best_individual, best_distance = get_best_solution(population, fitnesses)
    return best_individual, best_distance
