import numpy as np
import pyrosim.pyrosim as pyrosim
import random
import os
import time as t
import constants as c
from plan import PLAN


class SOLUTION:
    def __init__(self, nextAvailableID):
        self.myID = nextAvailableID
        self.x = 0
        self.y = 0
        self.z = 0.5
        self.length = 1
        self.width = 1
        self.height = 1
        self.plan = PLAN()
        self.links, self.joints = self.plan.Make_Blueprint()
        self.boolArray = self.plan.boolArray
        self.sensorCount = np.sum(self.boolArray)
        print(self.sensorCount)
        self.weights = np.random.rand(self.sensorCount, c.numMotorNeurons) * 2 - 1

    def Evaluate(self, directOrGUI):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        os.system(f"python3 simulate.py {directOrGUI} {self.myID} 2&>1 &")
        f = open(f"fitness{self.myID}.txt", "r")
        while not os.path.exists(f"fitness{self.myID}.txt"):
            t.sleep(0.01)
        self.fitness = float(f.read())
        print(self.fitness)
        f.close()

    def Start_Simulation(self, directOrGUI):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        os.system(f"python3 simulate.py {directOrGUI} {self.myID} 2&>1 &")

    def Wait_For_Simulation_To_End(self):
        while not os.path.exists(f"fitness{self.myID}.txt"):
            t.sleep(0.01)
        # with open(f"fitness{self.myID}.txt", "r", encoding='UTF-8' ) as file:
        #     lines = file.readline()
        #     self.fitness = float(lines)
        while True:
            f = open(f"fitness{self.myID}.txt", "r")
            content = f.read()
            if content != "":
                self.fitness = float(content)
                f.close()
                break
            else:
                f.close()
        os.system(f"rm fitness{self.myID}.txt")

    def Mutate(self):
        for link in self.links:
            linkID = link.linkID
            for dim in range(3):
                if self.fitness < -3:
                    randomDimChance = np.random.randint(0,6)
                elif self.fitness < -6:
                    randomDimChance = np.random.randint(0,8)
                else:
                    randomDimChance = np.random.randint(0,4)
                if randomDimChance == 0:
                    self.plan.Mutate_Dimension(linkID,dim)
        randomSynapseChance = np.random.randint(0,3)
        if randomSynapseChance == 0:
            self.Mutate_Synapse()

    def Mutate_Synapse(self):
        odds = 3 / (self.sensorCount * c.numMotorNeurons)
        for row in range(self.sensorCount):
            for col in range(c.numMotorNeurons):
                chance = np.random.rand()
                if chance <= odds:
                    self.weights[row][col] = np.random.rand() * 2 - 1

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        #pyrosim.Send_Cube(name="Box", pos=[self.x - 3, self.y - 3, self.z], size=[self.length, 100, self.height],mass=0)
        pyrosim.End()

    def Create_Body(self):
        pyrosim.Start_URDF(f"body{self.myID}.urdf")
        links = self.links
        joints = self.joints
        for i in range(len(links)):
            pyrosim.Send_Cube(name=links[i].name, pos=links[i].pos, size=links[i].size,
                              colorName=links[i].colorName, rgba=links[i].rgba)
        for j in range(len(joints)):
            pyrosim.Send_Joint(name=joints[j].name, parent=joints[j].parent, child=joints[j].child,
                               type=joints[j].jointtype, position=joints[j].position, jointAxis=joints[j].axis)
        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")
        count = 0
        for i in range(c.numSensorNeurons):
            if self.boolArray[i] == 1:
                pyrosim.Send_Sensor_Neuron(name=count, linkName=f"Body{i}")
                count += 1

        for j in range(len(self.joints)):
            pyrosim.Send_Motor_Neuron(name=count + j, jointName=self.joints[j].name)

        for currentRow in range(count):
            for currentColumn in range(c.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName=currentRow, targetNeuronName=currentColumn + count,
                                     weight=self.weights[currentRow][currentColumn])
        pyrosim.End()

    def Set_ID(self, ID):
        self.myID = ID