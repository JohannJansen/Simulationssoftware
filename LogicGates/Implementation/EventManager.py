import queue

from Event import create_gateevent


class EventManager:

    def __init__(self):
        self.queue = []

    def add_event(self, event):
        self.queue.append(event)
        self.queue.sort(key=lambda e: e.timestamp)

    def execute_event(self, event):
        if event.is_input_event:
            event.input.set_value(event.value)
            event.input.output_log.append(Out_log(event.timestamp, event.value))
            for output in event.input.outputs:
                self.add_event(create_gateevent(output, event.input.value, event.timestamp))
        else:
            gate = event.gate_connection.gate
            input_index = event.gate_connection.input_index
            gate.inputs[input_index] = event.value
            if gate.output_value is not gate.calculate(gate.inputs):
                gate.output_value = gate.calculate(gate.inputs)
                gate.output_log.append(Out_log(event.timestamp + gate.delay, gate.output_value))
                for output in gate.outputs:
                    existing_element = self.find_existing_element(event.timestamp + gate.delay, event)
                    if existing_element is not None:
                        existing_element.value = gate.output_value
                    else:
                        self.add_event(create_gateevent(output, gate.output_value, event.timestamp + gate.delay))

    def find_existing_element(self, timestamp, event):
        existing_element = None
        for element in self.queue:
            if element.timestamp is timestamp and element.gate_connection is event.gate_connection and element is not event:
                existing_element = element
        return existing_element


class Out_log:

    def __init__(self, timestamp, value):
        self.timestamp = timestamp
        self.value = value

    def __str__(self):
        return "Change to value: {value} at timestamp: {timestamp}".format(value=self.value, timestamp=self.timestamp)
