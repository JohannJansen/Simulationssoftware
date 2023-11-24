import matplotlib.pyplot as plt

# CONSTANTS
R = 10000
C = 47 * 10e-6
U_A = 1
U_E = 2
STEP_WIDTH = 0.1
MAXSTEPS = 1000
UPPERLIMIT = U_E * 0.999

class EulerIntegration:
    def __init__(self,step_width,function,start_value) -> None:
        self.n = 0
        self.nValue = start_value
        self.step_width = step_width
        self.bigF = function
        pass

    def next(self):
        self.nValue = self.nValue + self.step_width * self.bigF(self.nValue, self.step_width*self.n)
        self.n += 1
        return self.nValue
    

def function(f_n,n):
    return (U_E - f_n) / (R*C)

euler = EulerIntegration(STEP_WIDTH, function, U_A)

voltages = []
while euler.n < MAXSTEPS and euler.nValue < UPPERLIMIT:
    voltages.append(euler.next())

time = []
for i in range(0,len(voltages)):
    time.append(i*STEP_WIDTH)

plt.figure(figsize = (12, 8))
plt.plot(time, voltages, 'bo--', label='Approximate')
plt.title('Capacitor voltages in respect to time')
plt.xlabel('t')
plt.ylabel('U_A(t)')
plt.grid()
plt.legend(loc='lower right')
#plt.savefig('FallingBallSimulation{t}DeltaT.png'.format(t=STEPDISTANCE))
plt.show()

print(euler.n)
