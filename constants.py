import numpy as np

amplitudeFront = np.pi/4
amplitudeBack = np.pi/4
frequencyFront = 10.0
frequencyBack = 10.0
phaseOffsetFront = 0
phaseOffsetBack = np.pi/4
numberOfGenerations = 1
populationSize = 1
numLinks = np.random.randint(2,9)
#np.random.randint(2,4)
numMotorNeurons = numLinks-1
numSensorNeurons = numLinks
motorJointRange = .2
