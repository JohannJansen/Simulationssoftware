import random


class ChoiceGate:
    def __init__(self, is_probability_based, following, probabilities):
        self.is_probability_based = is_probability_based
        self.following = following
        self.probabilities = probabilities

    def determine_next(self):
        if self.is_probability_based:
            value = random.choices(self.following, weights=self.probabilities, k=1)[0]
            if type(value) is ChoiceGate:
                return value.determine_next()
        else:
            best_station = self.following[0]
            for station in self.following:
                if len(station.queue) < len(best_station.queue):
                    best_station = station
            value = best_station
        return value


def create_probability_gate(following, probabilities):
    return ChoiceGate(True, following, probabilities)


def create_distributor_gate(following):
    return ChoiceGate(False, following, None)


if __name__ == '__main__':
    cg = ChoiceGate(("test1", "test2"), (80, 20))
    values = []
    for i in range(100):
        values.append(cg.determine_next())

    print(values.count("test1"))
