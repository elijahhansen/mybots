import os

import pybullet as p
import pyrosim.pyrosim as pyrosim
from sensor import SENSOR
import time as t
from motor import MOTOR
from pyrosim.neuralNetwork import NEURAL_NETWORK


class ROBOT:
    def __init__(self, solutionID):
        self.solutionID = solutionID
        self.robotId = p.loadURDF("body.urdf")
        pyrosim.Prepare_To_Simulate(self.robotId)
        self.prepare_to_sense()
        self.prepare_to_act()
        self.nn = NEURAL_NETWORK(f"brain{self.solutionID}.nndf")
        os.system(f"rm brain{self.solutionID}.nndf")

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
                desiredAngle = self.nn.Get_Value_Of(neuronName)
                self.motors[jointName].set_value(self.robotId, desiredAngle)

    def think(self):
        self.nn.Update()

    def Get_Fitness(self):
        stateOfLinkZero = p.getLinkState(self.robotId, 0)
        positionOfLinkZero = stateOfLinkZero[0]
        xCoordinateOfLinkZero = positionOfLinkZero[0]
        f = open(f"tmp{self.solutionID}.txt", "w")
        f.write(str(xCoordinateOfLinkZero))
        os.system(f"mv tmp{self.solutionID}.txt fitness{self.solutionID}.txt")
        f.close()



