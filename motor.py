import numpy as np

import constants as c
import pyrosim.pyrosim as pyrosim
import pybullet as p


class MOTOR:
    def __init__(self, jointName):
        self.jointName = jointName
        self.prepare_to_act()

    def prepare_to_act(self):
        self.MotorValues = np.linspace(0,2*np.pi,1000)
        self.amplitude = c.amplitudeBack
        self.frequency = c.frequencyBack
        self.offset = c.phaseOffsetFront
        ##if len(self.jointName) == 14:
         ##   self.frequency = 1/2 * self.frequency
        for i in range(len(self.MotorValues)):
            self.MotorValues[i] = self.amplitude * np.sin(self.frequency * self.MotorValues[i] + self.offset)



    def set_value(self, robotId, desiredAngle):
        pyrosim.Set_Motor_For_Joint(bodyIndex=robotId, jointName=self.jointName, controlMode=p.POSITION_CONTROL,
                                    targetPosition=desiredAngle, maxForce=80)

    def save_values(self):
        np.save('data/motorvalues.npy', self.MotorValues)