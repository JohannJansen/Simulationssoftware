class Event:
    def __init__(self, is_add_event, station, student, timestamp):
        self.is_add_event = is_add_event
        self.station = station
        self.student = student
        self.timestamp = timestamp


def create_add_event(station, student, timestamp):
    return Event(True, station, student, timestamp)


def create_pop_event(station, student, timestamp):
    return Event(False, station, student, timestamp)
