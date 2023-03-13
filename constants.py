import numpy as np
import random

amplitudeFront = np.pi/4
amplitudeBack = np.pi/4
frequencyFront = 10.0
frequencyBack = 10.0
phaseOffsetFront = 0
phaseOffsetBack = np.pi/4
numberOfGenerations = 10
populationSize = 10
numLinks = np.random.randint(2,9)
#np.random.randint(2,4)
numMotorNeurons = numLinks
numSensorNeurons = numLinks+1
motorJointRange = .5
