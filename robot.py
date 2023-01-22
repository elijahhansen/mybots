import pybullet as p
import pyrosim.pyrosim as pyrosim
from sensor import SENSOR
import time as t
from motor import MOTOR


class ROBOT:
    def __init__(self):
        self.robotId = p.loadURDF("body.urdf")
        pyrosim.Prepare_To_Simulate(self.robotId)
        self.prepare_to_sense()
        self.prepare_to_act()

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

    def act(self, i):
        for jointName in self.motors:
            self.motors[jointName].set_value(self.robotId, i)



