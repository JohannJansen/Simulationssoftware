class Event:

    def __init__(self, is_input_event, gate_connection, input, value, timestamp):
        self.is_input_event = is_input_event
        self.gate_connection = gate_connection
        self.input = input
        self.value = value
        self.timestamp = timestamp


def create_inputevent(input, value, timestamp):
    return Event(True, None, input, value, timestamp)


def create_gateevent(gate_connection, value, timestamp):
    return Event(False, gate_connection, None, value, timestamp)
