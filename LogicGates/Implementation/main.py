from Event import create_inputevent, create_gateevent
from EventManager import EventManager
from Gate import Gate, create_or_gate, create_end_gate, create_and_gate, create_not_gate, Gateconnection
from Input import create_input
import matplotlib.pyplot as plt

def plotdata(deltaT, totaltime, element):
    values = []
    times = []
    iterations = 0
    while totaltime > deltaT * iterations:
        max = None
        for output_log in element.output_log:
            if output_log.timestamp <= deltaT * iterations:
                max = output_log
            else:
                break
        value = 1 if output_log.value else 0
        values.append(value)
        times.append(deltaT * iterations)
        iterations += 1

    plt.figure(figsize=(12, 8))
    plt.plot(times, values, 'bo--', label='Voltage')
    plt.title('Outputs in respect to time')
    plt.xlabel('t')
    plt.ylabel('output')
    plt.grid()
    plt.legend(loc='lower right')
    # plt.savefig('FallingBallSimulation{t}DeltaT.png'.format(t=STEPDISTANCE))
    plt.show()


if __name__ == '__main__':
    eventmanager = EventManager()
    # inputs
    inputA = create_input()
    inputB = create_input()
    inputC = create_input()
    inputD = create_input()

    # gates
    gateG1 = create_or_gate()
    gateG2 = create_not_gate()
    gateG3 = create_not_gate()
    gateG4 = create_and_gate()
    gateG5 = create_or_gate()
    gateG6 = create_or_gate()
    gateOut = create_end_gate()
    # connections for inputs
    inputA.addoutput(Gateconnection(gateG1, 0))
    inputB.addoutput(Gateconnection(gateG1, 1))
    inputB.addoutput(Gateconnection(gateG5, 0))
    inputC.addoutput(Gateconnection(gateG2, 0))
    inputD.addoutput(Gateconnection(gateG3, 0))
    # connections for gates
    gateG1.addoutput(Gateconnection(gateG4, 0))
    gateG2.addoutput(Gateconnection(gateG4, 1))
    gateG3.addoutput(Gateconnection(gateG5, 1))
    gateG4.addoutput(Gateconnection(gateG6, 0))
    gateG5.addoutput(Gateconnection(gateG6, 1))
    gateG6.addoutput(Gateconnection(gateOut, 0))
    # events binary 0 trough 15 with inputA as LSB and inputD as MSB

    eventtimer = 0
    for valueD in [False, True]:
        for valueC in [False, True]:
            for valueB in [False, True]:
                for valueA in [False, True]:
                    eventmanager.add_event(create_inputevent(inputA, valueA, eventtimer))
                    eventmanager.add_event(create_inputevent(inputB, valueB, eventtimer))
                    eventmanager.add_event(create_inputevent(inputC, valueC, eventtimer))
                    eventmanager.add_event(create_inputevent(inputD, valueD, eventtimer))

                    eventtimer += 30

    for valueD in [True, False]:
        for valueC in [True, False]:
            for valueB in [True, False]:
                for valueA in [True, False]:
                    eventmanager.add_event(create_inputevent(inputA, valueA, eventtimer))
                    eventmanager.add_event(create_inputevent(inputB, valueB, eventtimer))
                    eventmanager.add_event(create_inputevent(inputC, valueC, eventtimer))
                    eventmanager.add_event(create_inputevent(inputD, valueD, eventtimer))

                    eventtimer += 30

    for input in [inputA, inputB, inputC, inputD]:
        for output in input.outputs:
            output.gate.inputs[output.input_index] = input.value

    for gate in [gateG1, gateG2, gateG3, gateG4, gateG5, gateG6, gateOut]:
        gate.output_value = gate.calculate(gate.inputs)
        for output in gate.outputs:
            output.gate.inputs[output.input_index] = gate.output_value

    while len(eventmanager.queue) > 0:
        event = eventmanager.queue[0]
        eventmanager.queue.remove(event)
        eventmanager.execute_event(event)

    # print(*inputA.output_log, sep="\n")
    # print(*inputB.output_log, sep="\n")
    # print(*gateG1.output_log, sep="\n")
    print(*gateOut.output_log, sep="\n")

    plotdata(30, 1000, gateOut)

