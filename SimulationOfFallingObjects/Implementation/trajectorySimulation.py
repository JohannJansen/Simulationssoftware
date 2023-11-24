import numpy as np
import matplotlib.pyplot as plt

IMPACTPOINTAPPROXIMATIONMAXDEPTH = 4
MAXBOUNCES = 5
MAXTIME = 10

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
velocity = lambda t, vel : vel + -g * t
bounceBack = lambda t, vel : e * -velocity(t, vel)

# euler Integration function
def eulerIntegration(function, timeSincePrev, previousValue, timeSinceStart, currentVelocity):
    return previousValue + timeSincePrev * function(timeSinceStart, currentVelocity)

def eulerSimulateFallTrajectoryODE(function, startValue, stepDistance, maxtime, upperBound, lowerBound):
    # list to save results
    functionResultsApprox = []
    functionResultsApprox.append(startValue)
    currentTime = 0
    totalTime = 0
    numBounces = 0
    currentVelocity = v0


    # until either the maxtime is reached or either one of the bounds is crossed calculate ODE results using Euler
    while totalTime < MAXTIME and numBounces < MAXBOUNCES:
        functionResultsApprox.append(eulerIntegration(function, stepDistance, functionResultsApprox[-1], currentTime, currentVelocity))
        #TODO Smooth curve at the end
        if functionResultsApprox[-1] > upperBound or functionResultsApprox[-1] < lowerBound:
            target = lowerBound if functionResultsApprox[-1] <= lowerBound else upperBound
            impactTime = approximateTimeOfImpact(target, function, functionResultsApprox[-1], stepDistance, currentTime, IMPACTPOINTAPPROXIMATIONMAXDEPTH, currentVelocity)
            currentVelocity = bounceBack(impactTime, currentVelocity)
            numBounces += 1
            currentTime = 0
            # calculate approximation from approxTimeOfImpact until next full step. The height at approxTimeOfImpact is assumed to be the target height of either upper or lower bound
            functionResultsApprox[-1] = eulerIntegration(function, impactTime, target, currentTime - stepDistance + impactTime, currentVelocity)
        
        currentTime += stepDistance
        totalTime += stepDistance

    return functionResultsApprox    

def approximateTimeOfImpact(target, function, previousValue, stepDistance, currentTime, maxDepth, currentVelocity):
    currentDepth = 0
    newStepDistance = stepDistance/2
    bestResult = eulerIntegration(function, stepDistance,previousValue,currentTime, currentVelocity)
    bestStep = stepDistance
    while currentDepth < maxDepth:
        eulerResult = eulerIntegration(function, newStepDistance, previousValue, currentTime, currentVelocity)
        if abs(target - eulerResult) < abs(target - bestResult):
            bestResult = eulerResult
            bestStep = newStepDistance

        if eulerResult == target:
            return bestStep
        elif eulerResult < target:
            newStepDistance -= newStepDistance/2
        else:
            newStepDistance += newStepDistance/2
        currentDepth += 1
    return bestStep


yApprox = eulerSimulateFallTrajectoryODE(velocity, y0, deltaT, MAXTIME, 100, 0)

# initialize list of y values with y0 being the inital value
# y = []
# y.append(y0)

# iterate until either the max number of bounces or the max amount of time is reached
# while numBounces < maxBounces and currentTime <= endTime:
#     y.append(y[-1] + deltaT*velocity(currentTime))
#     # On bounce set the result to 0
#     # set v0 to the velocity after the bounce
#     # reset the current time used in the velocity calculation
#     if y[-1] <= yTable + r:
#         numBounces += 1
#         y[-1] = 0
#         v0 = e * -velocity(currentTime)
#         currentTime = 0
#     currentTime += deltaT
#     totalTime += deltaT

# initialize and fill array with values for time axis
time = []
for i in range(0,len(yApprox)):
    time.append(i*deltaT)

# # Reset values for Exact calculation
# y0 = 2
# v0 = 0
# currentTime = 0

# # initialize data structure for exact values
# yExact = []
# yExact.append(y0)

# # calculate exact values until reaching the ground
# while yExact[-1] > yTable + r:
#     yExact.append(exact(currentTime))
#     currentTime += deltaT
# yExact[-1] = 0

# # fill remaining time steps with zero for plotting
# while len(yExact) < len(y):
#     yExact.append(0)
    
# plot and save results
plt.figure(figsize = (12, 8))
plt.plot(time, yApprox, 'bo--', label='Approximate')
#plt.plot(time, y, 'bo--', label='Approximate')
#plt.plot(time, yExact, 'g', label='Exact')
plt.title('Approximate and Exact Solution \
for falling ping pong ball positions')
plt.xlabel('t')
plt.ylabel('y(t)')
plt.grid()
plt.legend(loc='lower right')
plt.savefig('FallingBallSimulation{bounces}Bounces{t}DeltaT.png'.format(bounces=numBounces,t=deltaT))