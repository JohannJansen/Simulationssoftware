class Gate:

    def __init__(self, inputs, calculate, delay):
        self.inputs = inputs
        self.outputs = []
        self.calculate = calculate
        self.delay = delay
        self.output_value = calculate(self.inputs)
        self.output_log = []

    def addoutput(self, gate_connection):
        self.outputs.append(gate_connection)

    def calculate(self):
        return self.calculate(self.inputs)


class Gateconnection:
    def __init__(self, gate, input_index):
        self.gate = gate
        self.input_index = input_index


def create_and_gate():
    return Gate([False, False], lambda inputs: inputs[0] and inputs[1], 9)


def create_or_gate():
    return Gate([False, False], lambda inputs: inputs[0] or inputs[1], 10)


def create_not_gate():
    return Gate([False], lambda inputs: not inputs[0], 8)


def create_end_gate():
    return Gate([False], lambda inputs: inputs[0], 0)