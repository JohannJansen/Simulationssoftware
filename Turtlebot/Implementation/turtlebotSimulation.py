import math

import numpy as np
import matplotlib.pyplot as plt

WHEELBASE = 24.0
WHEELRADIUS = 6.4
TIMESTEP = 0.1


class TurtleBot:

    def __init__(self):
        self.posCenter = np.array([0.0, 0.0])
        self.botNormal = np.array([1.0, 0.0])
        self.omega1 = 0
        self.omega2 = 0

    def wheelposition1(self):
        return self.posCenter + np.matmul(createRotationMatrix(math.pi / 2.0), self.botNormal) * (WHEELBASE / 2.0)

    def wheelposition2(self):
        return self.posCenter + np.matmul(createRotationMatrix(-math.pi / 2.0), self.botNormal) * (WHEELBASE / 2.0)

    def move(self, newOmega1, newOmega2, deltaT):
        self.omega1 = newOmega1
        self.omega2 = newOmega2

        # case 3
        if self.omega1 == 0 and self.omega2 != 0 or self.omega2 == 0 and self.omega1 != 0:
            if self.omega1 == 0:
                alpha = 1 / WHEELBASE * WHEELRADIUS * self.omega2 * deltaT
            else:
                alpha = 1 / WHEELBASE * WHEELRADIUS * self.omega1 * deltaT
            rotationCenter = self.wheelposition1() if self.omega1 == 0 else self.wheelposition2()
            rotationMatrix = createRotationMatrix(-alpha)
            self.posCenter = np.matmul(rotationMatrix, (self.posCenter - rotationCenter)) + rotationCenter
            self.botNormal = normalizeVector2d(np.matmul(rotationMatrix, self.botNormal))

        # case 2
        elif self.omega1 == -self.omega2 or self.omega2 == -self.omega1:
            if self.omega1 < 0:
                alpha = 2 / WHEELBASE * WHEELRADIUS * self.omega2 * deltaT
            else:
                alpha = 2 / WHEELBASE * WHEELRADIUS * self.omega1 * deltaT
            self.botNormal = np.matmul(createRotationMatrix(-alpha), self.botNormal)

        # case 4/5/6
        elif 0 != self.omega1 != self.omega2 != 0:
            if self.omega1 > self.omega2:  # turn clockwise
                alpha = WHEELRADIUS / WHEELBASE * deltaT * (self.omega1 - self.omega2)
                dist = WHEELRADIUS * self.omega2 * deltaT
                distToRotationCenter = dist / alpha
                rotationCenter = self.posCenter + np.matmul(createRotationMatrix(-math.pi / 2.0), self.botNormal) * (
                        WHEELBASE / 2.0 + distToRotationCenter)
            else:  # turn counterclockwise
                alpha = WHEELRADIUS / WHEELBASE * deltaT * (self.omega2 - self.omega1)
                dist = WHEELRADIUS * self.omega1 * deltaT
                distToRotationCenter = dist / alpha
                rotationCenter = self.posCenter + np.matmul(createRotationMatrix(math.pi / 2.0), self.botNormal) * (
                        WHEELBASE / 2.0 + distToRotationCenter)
            rotationMatrix = createRotationMatrix(-alpha)

            self.posCenter = np.matmul(rotationMatrix, (self.posCenter - rotationCenter)) + rotationCenter
            self.botNormal = normalizeVector2d(np.matmul(rotationMatrix, self.botNormal))

        # case 1
        elif self.omega1 == self.omega2:
            dist = WHEELRADIUS * self.omega1 * deltaT
            self.posCenter += dist


def createRotationMatrix(angle):
    return [[math.cos(angle), -math.sin(angle)],
            [math.sin(angle), math.cos(angle)]]


def normalizeVector2d(vector):
    length = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
    return vector / length


if __name__ == '__main__':
    TOTALSTEPS = 50

    turtlebot = TurtleBot()
    print(turtlebot.wheelposition1())
    print(turtlebot.wheelposition2())
    counter = 0
    time = []
    positionsX = []
    positionsY = []
    normalX = []
    normalY = []
    omegaValues = [[4, 4], [4, 2], [4, 0], [4, -2], [4, -4]]
    while counter < TOTALSTEPS:
        valueIndex = counter // (TOTALSTEPS // len(omegaValues))
        print(valueIndex)
        turtlebot.move(omegaValues[valueIndex][0], omegaValues[valueIndex][1], TIMESTEP)
        positionsX.append(turtlebot.posCenter[0])
        positionsY.append(turtlebot.posCenter[1])
        normalX.append(turtlebot.botNormal[0])
        normalY.append(turtlebot.botNormal[1])
        time.append(TIMESTEP * counter)
        counter += 1

    plt.figure(figsize=(12, 12))
    # plt.plot(positionsX, positionsY, 'bo--', label='position')
    ax = plt.axes(projection='3d')
    ax.plot3D(positionsX, positionsY, time, 'green')
    ax.plot3D(normalX, normalY, time, 'blue')
    plt.title('Normals of the turtlebot combined configuration')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid()
    plt.legend(loc='lower right')
    plt.show()
