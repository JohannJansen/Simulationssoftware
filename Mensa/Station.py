import random
from Event import create_add_event, create_pop_event


class Station:
    def __init__(self, identifier, delay, variance, choice_gate, is_final_station, collector):
        self.identifier = identifier
        self.delay = delay
        self.variance = variance
        self.queue = []
        self.choice_gate = choice_gate
        self.is_final_station = is_final_station
        self.collector = collector

    def randomize_delay(self):
        return self.delay + random.randint(-self.variance, self.variance)

    def add_student(self, student, timestamp):
        self.queue.append(student)
        student.station_timestamps[self.identifier] = timestamp
        if len(self.queue) == 1:
            pop_event = create_pop_event(self, student, timestamp + self.randomize_delay())
            return pop_event
        return None

    def pop_student(self, timestamp):
        events = []
        student = self.queue.pop(0)
        if self.is_final_station:
            self.collector.append(student)
        else:
            next_station = self.choice_gate.determine_next()
            add_event = create_add_event(next_station, student, timestamp)
            events.append(add_event)

        if len(self.queue) > 0:
            next_student = self.queue[0]
            pop_event = create_pop_event(self, next_student, timestamp + self.randomize_delay())
            events.append(pop_event)
        return events


def create_station(identifier, delay, variance, choice_gate):
    return Station(identifier, delay, variance, choice_gate, False, None)


def create_final_station(identifier, delay, variance, collector):
    return Station(identifier, delay, variance, None, True, collector)
