import pybullet as p
import time as t
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy as np
import random
import constants as c
from simulation import SIMULATION
import sys

directOrGUI = sys.argv[1]
simulation = SIMULATION(directOrGUI)
simulation.run()
simulation.Get_Fitness()
"""
amplitudeFront = c.amplitudeFront
amplitudeBack = c.amplitudeBack
frequencyFront = c.frequencyFront
frequencyBack = c.frequencyBack
phaseOffsetFront = c.phaseOffsetFront
phaseOffsetBack = c.phaseOffsetBack
backLegSensorValues = np.zeros(1000)
frontLegSensorValues = np.zeros(1000)
x = np.linspace(0,2*np.pi, 1000)
TargetAnglesFront = amplitudeFront*np.sin(frequencyFront*x+phaseOffsetFront)
TargetAnglesBack = amplitudeBack*np.sin(frequencyBack*x+phaseOffsetBack)
##np.save('data/TargetAngles.npy',TargetAngles)
##exit()
for i in range(0,1000):
    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
    pyrosim.Set_Motor_For_Joint(bodyIndex=robotId, jointName=b'Torso_BackLeg', controlMode=p.POSITION_CONTROL,
                                targetPosition=TargetAnglesBack[i], maxForce=80)
    pyrosim.Set_Motor_For_Joint(bodyIndex=robotId, jointName=b'Torso_FrontLeg', controlMode=p.POSITION_CONTROL,
                                targetPosition= TargetAnglesFront[i], maxForce=80)
    t.sleep(1/2400)
p.disconnect()
print(backLegSensorValues)
np.save('data/backLegSensorValues.npy', backLegSensorValues)
np.save('data/frontLegSensorValues.npy', frontLegSensorValues)
"""
