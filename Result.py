import math
import random


class Result:

    def __init__(self, cities):
        self.cities = []
        for city in cities:
            self.cities.append(city)
        self.distance = 0
        self.calculate()

    def calculate(self):  # calculate the distance
        self.distance = 0
        for pair in zip(self.cities[1:], self.cities):
            self.distance += math.sqrt((pair[0].x - pair[1].x) ** 2 + (pair[0].y - pair[1].y) ** 2)
        self.distance += math.sqrt((self.cities[0].x - self.cities[-1].x) ** 2 +
                                   (self.cities[0].y - self.cities[-1].y) ** 2)

    def copy(self, result):
        self.cities = []
        for city in result.cities:
            self.cities.append(city)
        self.calculate()

    def print(self):
        output = ''
        for city in self.cities:
            output += city.name + ' '
        output += str(self.distance) + '\n'
        return output

    # reverse the cities in cities[start, end) if start <= end, else reverse over the length of the list
    def mutate(self):
        start = random.randint(0, len(self.cities) - 1)
        end = random.randint(0, len(self.cities) - 1)
        if start <= end:
            self.cities[start: end] = self.cities[start: end][::-1]
        else:
            self.cities[end: start] = self.cities[end: start][::-1]
            # copy = self.cities[start:] + self.cities[:end]
            # copy = copy[::-1]
            # self.cities[start:] = copy[:len(self.cities) - start]
            # self.cities[:end] = copy[len(self.cities) - start:]
        self.calculate()
