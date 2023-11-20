import numpy as np
import matplotlib.pyplot as plt

#Constants
IMPACTPOINTAPPROXIMATIONMAXDEPTH = 4
MAXBOUNCES = 5
MAXTIME = 10
GRAVITATIONALPULL = 9.81
REBOUND = 0.8
BALLRADIUS = 0
STARTHEIGHT = 2
TABLEHEIGHT = 0
STARTVELOCITY = 0
STEPDISTANCE = 0.1
AIRRESISTANCE = 0.17

# euler Integration function
def eulerIntegration(function, timeSincePrev, previousValue, timeSinceStart):
    return previousValue + timeSincePrev * function(timeSinceStart)

def eulerSimulateFallTrajectoryODE():
    #variables
    currentVelocity = 0
    currentTime = 0
    totalTime = 0
    numBounces = 0

    # list to save results
    functionResultsApprox = []
    functionResultsApprox.append(STARTHEIGHT)
    velocity = lambda t : STARTVELOCITY + -GRAVITATIONALPULL * currentTime + (-AIRRESISTANCE * (STARTVELOCITY + -GRAVITATIONALPULL * currentTime))

    # until either the maxtime is reached or either one of the bounds is crossed calculate ODE results using Euler
    while totalTime < MAXTIME and numBounces < MAXBOUNCES:
        functionResultsApprox.append(eulerIntegration(velocity, STEPDISTANCE, functionResultsApprox[-1], currentTime))

        if functionResultsApprox[-1] < TABLEHEIGHT:
            impactTime = approximateTimeOfImpact(TABLEHEIGHT, velocity, functionResultsApprox[-1], STEPDISTANCE, currentTime, IMPACTPOINTAPPROXIMATIONMAXDEPTH)
            currentVelocity = REBOUND * -velocity(currentTime)
            numBounces += 1
            currentTime = 0
            velocity = lambda t : currentVelocity + - GRAVITATIONALPULL * currentTime + (-AIRRESISTANCE * STARTVELOCITY + -GRAVITATIONALPULL * currentTime)
            functionResultsApprox[-1] = eulerIntegration(velocity, impactTime, TABLEHEIGHT, currentTime - STEPDISTANCE + impactTime)
        
        currentTime += STEPDISTANCE
        totalTime += STEPDISTANCE
    
    return functionResultsApprox

def approximateTimeOfImpact(target, function, previousValue, stepDistance, currentTime, maxDepth):
    currentDepth = 0
    newStepDistance = stepDistance/2
    bestResult = eulerIntegration(function, stepDistance,previousValue,currentTime)
    bestStep = stepDistance
    while currentDepth < maxDepth:
        eulerResult = eulerIntegration(function, newStepDistance, previousValue, currentTime)
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

yApprox = eulerSimulateFallTrajectoryODE()
time = []
for i in range(0,len(yApprox)):
    time.append(i*STEPDISTANCE)

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
plt.savefig('FallingBallSimulation{t}DeltaT.png'.format(t=STEPDISTANCE))