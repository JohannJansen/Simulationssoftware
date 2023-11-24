import numpy as np
import matplotlib.pyplot as plt
import math

#Constants
IMPACTPOINTAPPROXIMATIONMAXDEPTH = 4
MAXBOUNCES = 5
MAXTIME = 10
GRAVITATIONALPULL = 9.81
REBOUND = 0.8
BALLRADIUS = 0.0
STARTHEIGHT = 2.0
TABLEHEIGHT = 0.0
STARTVELOCITY = 0.0
STEPDISTANCE = 0.01
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
    # initiate problem specific function for euler
    velocity = lambda t : (STARTVELOCITY + -GRAVITATIONALPULL * t) * (1-AIRRESISTANCE)
    
    # until either the maxtime is reached or the max number of bounces are reached iterate for new y values
    while totalTime < MAXTIME and numBounces < MAXBOUNCES:
        # every iteration append a new y value to the results
        functionResultsApprox.append(eulerIntegration(velocity, STEPDISTANCE, functionResultsApprox[-1], currentTime))

        # on bounce
        if functionResultsApprox[-1] < TABLEHEIGHT:
            # calculate better approximation of impact time
            impactTime = approximateTimeOfImpact(TABLEHEIGHT, velocity, functionResultsApprox[-1], STEPDISTANCE, currentTime, IMPACTPOINTAPPROXIMATIONMAXDEPTH)
            # update variables on rebound
            currentVelocity = REBOUND * -velocity(currentTime)
            numBounces += 1
            currentTime = 0
            # redefine function to account for updated initial velocity
            velocity = lambda t : (currentVelocity + -GRAVITATIONALPULL * t) * (1-AIRRESISTANCE)
            # set last result to more exact value by calculating euler with the remaining time after approximation of impact time
            functionResultsApprox[-1] = eulerIntegration(velocity, impactTime, TABLEHEIGHT, currentTime - STEPDISTANCE + impactTime)
        
        currentTime += STEPDISTANCE
        totalTime += STEPDISTANCE
    
    return functionResultsApprox

def approximateTimeOfImpact(target, function, previousValue, stepDistance, currentTime, maxDepth):
    currentDepth = 0
    newStepDistance = stepDistance/2
    bestResult = eulerIntegration(function, stepDistance,previousValue,currentTime)
    bestStep = stepDistance
    # until maxdepth is reached search for value closer to zero
    while currentDepth < maxDepth:
        eulerResult = eulerIntegration(function, newStepDistance, previousValue, currentTime)
        # save best result and return at the end
        if abs(target - eulerResult) < abs(target - bestResult):
            bestResult = eulerResult
            bestStep = newStepDistance

        # set newStepDistance depending on euler result
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
plt.title('Approximations for falling ping pong ball positions')
plt.xlabel('t')
plt.ylabel('y(t)')
plt.grid()
plt.legend(loc='lower right')
plt.savefig('FallingBallSimulation{t}DeltaT.png'.format(t=STEPDISTANCE))