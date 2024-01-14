class EventManager:
    def __init__(self):
        self.queue = []

    def add_event(self, event):
        self.queue.append(event)
        self.queue.sort(key=lambda e: e.timestamp)

    def execute_event(self, event):
        if event.is_add_event:
            event_optional = event.station.add_student(event.student, event.timestamp)
            if event_optional:
                self.add_event(event_optional)
        else:
            events = event.station.pop_student(event.timestamp)
            for e in events:
                self.add_event(e)
