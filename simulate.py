import pybullet as p
import time as t
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy as np
import random

amplitudeFront = np.pi/4
amplitudeBack = 0
frequencyFront = 10
frequencyBack = 10
phaseOffsetFront = 0
phaseOffsetBack = np.pi/4
physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0,0,-9.8)
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")
p.loadSDF("world.sdf")
pyrosim.Prepare_To_Simulate(robotId)
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

