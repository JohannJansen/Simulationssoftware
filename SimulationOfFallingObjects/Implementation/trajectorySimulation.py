import numpy as np
import matplotlib.pyplot as plt

# Initializing Variables
y0 = 2
v0 = 0
g = 9.81
deltaT = 0.1
e = 0.8
r = 0
yTable = 0
endTime = 10.0
currentTime = 0
totalTime = 0
numBounces = 0
maxBounces = 100

# defining functions
exact = lambda t : y0 + v0 * t + 0.5 * -g * pow(t,2)
velocity = lambda t : v0 + -g * t

# initialize list of y values with y0 being the inital value
y = []
y.append(y0)

# iterate until either the max number of bounces or the max amount of time is reached
while numBounces < maxBounces and currentTime <= endTime:
    y.append(y[-1] + deltaT*velocity(currentTime))
    # On bounce set the result to 0
    # set v0 to the velocity after the bounce
    # reset the current time used in the velocity calculation
    if y[-1] <= yTable + r:
        numBounces += 1
        y[-1] = 0
        v0 = e * -velocity(currentTime)
        currentTime = 0
    currentTime += deltaT
    totalTime += deltaT

# initialize and fill array with values for time axis
time = []
for i in range(0,len(y)):
    time.append(i*deltaT)

# Reset values for Exact calculation
y0 = 2
v0 = 0
currentTime = 0

# initialize data structure for exact values
yExact = []
yExact.append(y0)

# calculate exact values until reaching the ground
while yExact[-1] > yTable + r:
    yExact.append(exact(currentTime))
    currentTime += deltaT
yExact[-1] = 0

# fill remaining time steps with zero for plotting
while len(yExact) < len(y):
    yExact.append(0)
    
# plot and save results
plt.figure(figsize = (12, 8))
plt.plot(time, y, 'bo--', label='Approximate')
plt.plot(time, yExact, 'g', label='Exact')
plt.title('Approximate and Exact Solution \
for falling ping pong ball positions')
plt.xlabel('t')
plt.ylabel('y(t)')
plt.grid()
plt.legend(loc='lower right')
plt.savefig('FallingBallSimulation{bounces}Bounces{t}DeltaT.png'.format(bounces=numBounces,t=deltaT))