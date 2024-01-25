import math
import random

import matplotlib.pyplot as plt


ZONEHEIGHT = 100
ZONEWIDTH = 100
NUMPEOPLE = 100
INFECTIONDURATION = 100
INFECTIONRADIUS = 5
INFECTIONCHANCE = 0.2
MAXMOVESPEED = 2
INITIALINFECTED = 10


class Person:
    def __init__(self):
        self.movementspeed = random.uniform(1, MAXMOVESPEED)
        self.infectiontimer = 0
        self.infected = False
        self.recovered = False
        self.direction = [random.uniform(-1, 1), random.uniform(-1, 1)]
        self.position = [random.uniform(0, ZONEWIDTH), random.uniform(0, ZONEHEIGHT)]

    def infect(self):
        self.infected = True
        self.infectiontimer = INFECTIONDURATION

    def update_position(self):
        newposx = self.position[0] + self.direction[0] * self.movementspeed
        newposy = self.position[1] + self.direction[1] * self.movementspeed

        if newposx < 0:
            newposx = 0
            self.direction[0] = -self.direction[0]
        if newposx > 100:
            newposx = 100
            self.direction[0] = -self.direction[0]

        if newposy < 0:
            newposy = 0
            self.direction[1] = -self.direction[1]
        if newposy > 100:
            newposy = 100
            self.direction[1] = -self.direction[1]

        self.position = [newposx, newposy]

    def check_for_infection(self, infected_list):
        for infected in infected_list:
            distance = math.dist(self.position, infected.position)

            if distance < INFECTIONRADIUS:
                is_infected = random.random() < INFECTIONCHANCE
                if is_infected:
                    self.infect()

    def update_infected(self):
        self.infectiontimer -= 1
        if self.infectiontimer == 0:
            self.recovered = True
            self.infected = False


def organize_lists(healthy, infected):
    for person in healthy:
        if person.infected:
            infected.append(person)
            healthy.remove(person)

    for person in infected:
        if person.recovered:
            infected.remove(person)


class Data:
    def __init__(self):
        self.infected_data = []
        self.healthy_data = []
        self.recovered_data = []

    def log(self, num_infected, num_healthy, num_recovered):
        self.infected_data.append(num_infected)
        self.healthy_data.append(num_healthy)
        self.recovered_data.append(num_recovered)

    def generate_times(self):
        return range(len(self.infected_data))


if __name__ == '__main__':
    data = Data()
    people = []
    healthy = []
    infected = []

    for _ in range(NUMPEOPLE):
        person = Person()
        people.append(person)
        healthy.append(person)

    initial_infected = random.choices(healthy, k=INITIALINFECTED)
    for person in initial_infected:
        person.infect()

    organize_lists(healthy, infected)

    while len(infected) > 0:
        organize_lists(healthy, infected)

        for person in people:
            person.update_position()

        for person in healthy:
            person.check_for_infection(infected)

        for person in infected:
            person.update_infected()

        data.log(len(infected), len(healthy), len(people) - len(infected) - len(healthy))

    times = data.generate_times()
    plt.figure(figsize=(12, 8))
    plt.plot(times, data.infected_data, label='Infected')
    plt.plot(times, data.healthy_data, label='Healthy')
    plt.plot(times, data.recovered_data, label='Recovered')
    plt.title("Pandemic Simulation")
    plt.xlabel('timesteps')
    plt.ylabel('People')
    plt.grid()
    plt.legend(loc='lower right')
    plt.savefig('Pandemic{num_people}people{initial}initial.png'.format(num_people=NUMPEOPLE, initial=INITIALINFECTED))
