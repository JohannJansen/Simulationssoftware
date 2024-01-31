import math
import random

import numpy
import numpy as np
from enum import Enum

import matplotlib.pyplot as plt

ZONEHEIGHT = 100
ZONEWIDTH = 100
NUMPEOPLE = 20
INFECTIONDURATION = 100
INFECTIONRADIUS = 5
INFECTIONCHANCE = 0.2
MAXMOVESPEED = 2
INITIALINFECTED = 3
INFECTEDTOFOLLOWINGCHANCE = 0.005
FATALITYRATE = 0.02
NOIMMINUTYCHANCE = 0.1
SOCIALDISTANCING = False
QUARANTINE = False


class State(Enum):
    HEALTHY = 1
    INFECTED = 2
    SYMPTOMS = 3
    QUARANTINE = 4
    RECOVERED = 5
    DECEASED = 6


class Person:
    def __init__(self):
        self.movementspeed = random.uniform(1, MAXMOVESPEED)
        self.timer = 0
        self.state = State.HEALTHY
        self.direction = [random.uniform(-1, 1), random.uniform(-1, 1)]
        self.position = [random.uniform(0, ZONEWIDTH), random.uniform(0, ZONEHEIGHT)]

    def update_state(self):
        # case infected
        if self.state is State.INFECTED:
            self.timer -= 1
            # roll chance for infection turning into symptoms or
            # quarantine each with 50% of happening if the 0.5% is rolled
            chance = random.random()
            if chance < INFECTEDTOFOLLOWINGCHANCE:
                if QUARANTINE:
                    self.start_quarantine()
                else:
                    self.start_symptoms()
                return
            if self.timer == 0:
                self.state = State.RECOVERED
        # case symptoms
        elif self.state is State.SYMPTOMS:
            self.timer -= 1
            if self.timer == 0:
                chance = random.random()
                if chance < NOIMMINUTYCHANCE:
                    self.infect()
                elif chance < FATALITYRATE + NOIMMINUTYCHANCE:
                    self.state = State.DECEASED
                else:
                    self.state = State.RECOVERED
        # case quarantine
        elif self.state is State.QUARANTINE:
            self.timer -= 1
            if self.timer == 0:
                chance = random.random()
                if chance < NOIMMINUTYCHANCE:
                    self.infect()
                elif chance < FATALITYRATE + NOIMMINUTYCHANCE:
                    self.state = State.DECEASED
                else:
                    self.state = State.RECOVERED

    def infect(self):
        self.state = State.INFECTED
        self.timer = INFECTIONDURATION

    def start_symptoms(self):
        self.state = State.SYMPTOMS
        self.timer = 50

    def start_quarantine(self):
        self.state = State.QUARANTINE
        self.timer = 50

    def update_position(self):
        if self.state in [State.QUARANTINE, State.RECOVERED, State.DECEASED]:
            return

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

    def update_position_social_distancing(self, personlist):
        new_direction = [0.0, 0.0]
        for person in personlist:
            if person.state in [State.HEALTHY, State.INFECTED, State.SYMPTOMS] and person is not self:
                opposite_direction = numpy.subtract(person.position, self.position)
                opposite_direction = opposite_direction * -1
                # normalize to have each surrounding person impact the new direction equally
                opposite_direction = opposite_direction / np.linalg.norm(opposite_direction)
                new_direction += opposite_direction
        new_direction = new_direction / np.linalg.norm(new_direction)
        self.direction = new_direction
        self.update_position()

    def check_for_infection(self, personlist):
        for person in personlist:
            if person.state in [State.INFECTED, State.SYMPTOMS]:
                distance = math.dist(self.position, person.position)

                if distance < INFECTIONRADIUS:
                    is_infected = random.random() < INFECTIONCHANCE
                    if is_infected:
                        self.infect()


class Data:
    def __init__(self):
        self.healthy_data = []
        self.infected_data = []
        self.symptoms_data = []
        self.quarantine_data = []
        self.recovered_data = []
        self.deceased_data = []

    def log(self, num_healthy, num_infected, num_symptoms, num_quarantine, num_recovered, num_deceased):
        self.healthy_data.append(num_healthy)
        self.infected_data.append(num_infected)
        self.symptoms_data.append(num_symptoms)
        self.quarantine_data.append(num_quarantine)
        self.recovered_data.append(num_recovered)
        self.deceased_data.append(num_deceased)

    def generate_times(self):
        return range(len(self.infected_data))


if __name__ == '__main__':
    data = Data()
    people = []

    for _ in range(NUMPEOPLE):
        person = Person()
        people.append(person)

    initial_infected = random.choices(people, k=INITIALINFECTED)
    for person in initial_infected:
        person.infect()

    # as long as there is at least one person remaining with the state infected,
    # symptoms or in quarantine continue simulation
    while len([person for person in people if person.state in [State.INFECTED, State.SYMPTOMS, State.QUARANTINE]]) > 0:

        for person in people:
            if SOCIALDISTANCING:
                person.update_position_social_distancing(people)
            else:
                person.update_position()
            person.update_state()
            if person.state is State.HEALTHY:
                person.check_for_infection(people)

        num_healthy = len([person for person in people if person.state is State.HEALTHY])
        num_infected = len([person for person in people if person.state is State.INFECTED])
        num_symptoms = len([person for person in people if person.state is State.SYMPTOMS])
        num_quarantine = len([person for person in people if person.state is State.QUARANTINE])
        num_recovered = len([person for person in people if person.state is State.RECOVERED])
        num_deceased = len([person for person in people if person.state is State.DECEASED])

        data.log(num_healthy, num_infected, num_symptoms, num_quarantine, num_recovered, num_deceased)

    times = data.generate_times()
    plt.figure(figsize=(12, 8))
    plt.plot(times, data.healthy_data, label='Healthy')
    plt.plot(times, data.infected_data, label='Infected')
    plt.plot(times, data.symptoms_data, label='Symptoms')
    plt.plot(times, data.quarantine_data, label='Quarantine')
    plt.plot(times, data.recovered_data, label='Recovered')
    plt.plot(times, data.deceased_data, label='Deceased')
    plt.title("Pandemic Simulation")
    plt.xlabel('timesteps')
    plt.ylabel('Number of persons')
    plt.grid()
    plt.legend(loc='upper right')
    plt.savefig('Pandemic{num_people}people{initial}initial_socialdistance_is_{sd}_quarantine_is_{quarantine}.png'
                .format(num_people=NUMPEOPLE, initial=INITIALINFECTED, sd=SOCIALDISTANCING, quarantine=QUARANTINE))
