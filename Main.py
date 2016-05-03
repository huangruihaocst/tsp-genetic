import json
import random
import numpy as np
import sys
from random import shuffle
import City
import Result

THRESHOLD = 1e-5
M = 1e5

in_file = sys.argv[1]
out_file = sys.argv[2]

# reading in
content = open(in_file).read()
lines = content.split('\n')
n = int(lines[0])
cities = []
for line in lines:
    if lines.index(line) != 0 and line != '':
        info = line.split('\t')
        cities.append(City.City(info[0], float(info[1]), float(info[2])))

config = json.loads(open('config.json').read())
quantity = config['population_quantity']
reproduce = config['reproduce_possibility']
mutate = config['mutate_possibility']
stop = config['stop_generation']

solution = Result.Result(cities)  # current best solution
minimum = solution.distance

population = []  # always the same size = quantity
for i in range(0, quantity):  # the first population
    shuffle(cities)
    result = Result.Result(cities)
    population.append(result)
for result in population:  # update best solution
    if result.distance < minimum:
        solution.copy(result)
        minimum = result.distance

for generation in range(0, stop):  # reproduce and mutate for several generations
    # step1: generate a new population using roulette method
    fitness = []
    for result in population:  # calculate fitness
        if result.distance > minimum:
            f = 1 / (result.distance - minimum)
        else:
            f = M
        fitness.append(f)
    possibilities = []
    for f in fitness:  # calculate possibility using
        possibilities.append(f / sum(fitness))
    population = list(np.random.choice(population, quantity, possibilities))  # a new population

    # step2: reproduce
    for pair in list(zip(*([iter(population)] * 2))):
        if random.uniform(0, 1) < reproduce:
            pos = random.randint(0, len(cities) - 1)
            pair[0].cities[pos:] = [x for x in pair[1].cities if x not in pair[0].cities[:pos]]
            pair[0].calculate()
            pair[1].cities[pos:] = [x for x in pair[0].cities if x not in pair[1].cities[:pos]]
            pair[1].calculate()
    for result in population:  # update best solution
        if result.distance < minimum:
            solution.copy(result)
            minimum = result.distance

    # step3: mutate
    for res in population:
        if random.uniform(0, 1) < mutate:
            res.mutate()
    for result in population:  # update best solution
        if result.distance < minimum:
            solution.copy(result)
            minimum = result.distance

open(out_file, 'w').write(solution.print())
