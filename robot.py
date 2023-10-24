import os

import pybullet as p
import pyrosim.pyrosim as pyrosim
from sensor import SENSOR
import time as t
from motor import MOTOR
from pyrosim.neuralNetwork import NEURAL_NETWORK
import constants as c


class ROBOT:
    def __init__(self, solutionID):
        self.solutionID = solutionID
        self.robotId = p.loadURDF(f"body{solutionID}.urdf")
        pyrosim.Prepare_To_Simulate(self.robotId)
        self.prepare_to_sense()
        self.prepare_to_act()
        self.nn = NEURAL_NETWORK(f"brain{self.solutionID}.nndf")
        os.system(f"rm brain{self.solutionID}.nndf")
        os.system(f"rm body{self.solutionID}.urdf")

    def prepare_to_sense(self):
        self.sensors = {}
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)

    def sense(self,i):
        for linkName in self.sensors:
            self.sensors[linkName].get_value(i)

    def prepare_to_act(self):
        self.motors = {}
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)

    def act(self):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName) * c.motorJointRange
                self.motors[jointName].set_value(self.robotId, desiredAngle)

    def think(self):
        self.nn.Update()

    def Get_Fitness(self):
        basePositionAndOrientation = p.getBasePositionAndOrientation(self.robotId)
        basePosition = basePositionAndOrientation[0]
        xPosition = basePosition[0]
       # with open(f"tmp{self.solutionID}.txt", "w")  as txt_file:
        #    txt_file.write(str(xPosition))
         #   os.system(f"mv tmp{self.solutionID}.txt fitness{self.solutionID}.txt")
        f = open(f"tmp{self.solutionID}.txt", "x")
        f.write(f"{xPosition}")
        os.system(f"mv tmp{self.solutionID}.txt fitness{self.solutionID}.txt")
        f.close()



