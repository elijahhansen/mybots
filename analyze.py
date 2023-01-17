import numpy as np
import matplotlib.pyplot


backlegsensorvalues = np.load('data/backLegSensorValues.npy')
frontlegsensorvalues = np.load('data/frontLegSensorValues.npy')
TargetAngles = np.load('data/TargetAngles.npy')
print(backlegsensorvalues)
##matplotlib.pyplot.plot(backlegsensorvalues, label = 'BackLeg', linewidth=2)
##matplotlib.pyplot.plot(frontlegsensorvalues, label = 'FrontLeg')
matplotlib.pyplot.plot(TargetAngles, label = 'TargetAngles')
matplotlib.pyplot.legend()
matplotlib.pyplot.show()
