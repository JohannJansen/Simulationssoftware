class Input:
    def __init__(self):
        self.value = False
        self.outputs = []
        self.output_log = []

    def set_value(self, value):
        self.value = value

    def addoutput(self, gate_connection):
        self.outputs.append(gate_connection)


def create_input():
    return Input()
