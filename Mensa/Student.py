class Student:
    def __init__(self, id, entrytime):
        self.id = id
        self.entrytime = entrytime
        self.station_timestamps = {}


def create_student(id, entrytime):
    return Student(id, entrytime)
