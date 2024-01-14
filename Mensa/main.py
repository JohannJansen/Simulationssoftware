import csv
import Student
from ChoiceGate import ChoiceGate, create_probability_gate, create_distributor_gate
from Event import create_add_event
from EventManager import EventManager
from Station import create_final_station, create_station

# entrytime in CSV is in minutes time for simulation in seconds
TIMESCALAR_ENTRYTIME = 60


def import_student_csv(path):
    students = []
    with open(path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == "id":
                continue
            else:
                student_id = int(row[0])
                entrytime = int(row[1]) * TIMESCALAR_ENTRYTIME
                student = Student.create_student(student_id, entrytime)
                students.append(student)
    return students


def display_in_minutes(time):
    minutes = time // 60
    seconds = time % 60
    return "{minutes}:{seconds}".format(minutes=minutes, seconds=seconds)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    students = import_student_csv("EntryTimes/normal_linksseitig.csv")
    eventmanager = EventManager()

    # start => e1,e2,e3,e4,NachtischEntscheidung
    # e1-e4 => NachtischEntscheidung
    # NachtischEntscheidung => Kassenentscheidung, Nachtisch
    # Nachtisch => Kassenentscheidung
    # Kassenentscheidung => Kartenkasse, NormaleKassenEntscheidung
    # NormaleKassenentscheidung => k1,k2
    # k1,k2 => Ende

    collector = []
    end = create_final_station("ende", 0, 0, collector)
    end_gate = create_probability_gate([end], [100])

    k1 = create_station("BarKasse1", 10, 2, end_gate)
    k2 = create_station("BarKasse2", 15, 5, end_gate)
    k3 = create_station("KartenKasse", 10, 1, end_gate)
    cash_point_gate = create_distributor_gate([k1, k2])
    card_gate = create_probability_gate([cash_point_gate, k3], [80, 20])

    dessert_station = create_station("Dessert", 15, 5, card_gate)
    dessert_gate = create_probability_gate([card_gate, dessert_station], [5, 95])

    e1 = create_station("Essen1", 10, 2, dessert_gate)
    e2 = create_station("Essen2", 15, 3, dessert_gate)
    e3 = create_station("Essen3", 20, 1, dessert_gate)
    e4 = create_station("Essen4", 20, 10, dessert_gate)
    # TODO Tafelbild abgleich
    meal_gate = create_probability_gate([e1, e2, e3, e4, dessert_gate], [40, 25, 20, 10, 5])

    start_gate = create_station("Eingang", 0, 0, meal_gate)

    for student in students:
        add_event = create_add_event(start_gate, student, student.entrytime)
        eventmanager.add_event(add_event)

    while len(eventmanager.queue) > 0:
        eventmanager.execute_event(eventmanager.queue.pop(0))

    print(len(collector))
    for student in collector:
        print(display_in_minutes(student.station_timestamps["ende"] - student.entrytime))
