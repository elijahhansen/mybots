import numpy as np

amplitudeFront = np.pi/4
amplitudeBack = np.pi/4
frequencyFront = 15.0
frequencyBack = 15.0
phaseOffsetFront = 0
phaseOffsetBack = np.pi/4
numberOfGenerations = 10
populationSize = 10
numLinks = np.random.randint(2,9)
numMotorNeurons = numLinks-1
numSensorNeurons = numLinks
motorJointRange = .2
