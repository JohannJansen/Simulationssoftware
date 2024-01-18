import csv
import Student
import matplotlib.pyplot as plt
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


if __name__ == '__main__':
    students = import_student_csv("EntryTimes/triangular.csv")
    eventmanager = EventManager()

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
    
    meal_gate = create_probability_gate([e1, e2, e3, e4, dessert_gate], [40, 25, 20, 10, 5])

    start_gate = create_station("Eingang", 0, 0, meal_gate)

    for student in students:
        add_event = create_add_event(start_gate, student, student.entrytime)
        eventmanager.add_event(add_event)

    while len(eventmanager.queue) > 0:
        eventmanager.execute_event(eventmanager.queue.pop(0))

    students_per_minute = []
    for i in range(120):
        minute_list = [student for student in students if student.entrytime // 60 == i]
        students_per_minute.append(minute_list)

    avg_duration_per_minute = []
    for minute_list in students_per_minute:
        sum = 0
        if len(minute_list) > 0:
            for student in minute_list:
                sum += student.station_timestamps["ende"] - student.entrytime
            sum = sum / len(minute_list) // 60
        avg_duration_per_minute.append(sum)
    
    print(len(students_per_minute))

    minutes = []
    for minute in range(120):
        minutes.append(minute)

    datadistribution = "triangular"
    experiment = "avg_duration_per_minute"
    plt.figure(figsize = (12, 8))
    plt.plot(minutes, avg_duration_per_minute, 'bo--', label=experiment)
    plt.title('Average wait time per minute')
    plt.xlabel('minutes')
    plt.ylabel('seconds')
    plt.grid()
    plt.legend(loc='lower right')
    plt.savefig('{experiment}_{datadistribution}.png'.format(experiment=experiment, datadistribution=datadistribution))
    plt.show()
