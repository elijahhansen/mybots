import numpy as np
import pyrosim.pyrosim as pyrosim
import random
import os
import time as t
import constants as c


class SOLUTION:
    def __init__(self, nextAvailableID):
        self.myID = nextAvailableID
        self.weights = np.random.rand(c.numSensorNeurons, c.numMotorNeurons)
        self.weights = self.weights * c.numMotorNeurons - 1
        self.x = 0
        self.y = 0
        self.z = 0.5
        self.length = 1
        self.width = 1
        self.height = 1
        self.boolArray = np.random.randint(2, size=c.numLinks+1)

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
        randomRow = random.randint(0, c.numSensorNeurons-1)
        randomColumn = random.randint(0, c.numMotorNeurons-1)
        self.weights[randomRow, randomColumn] = random.random() * c.numSensorNeurons - 1



    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        #pyrosim.Send_Cube(name="Box", pos=[self.x - 3, self.y - 3, self.z], size=[self.length, 100, self.height],mass=0)
        pyrosim.End()

    def Create_Body(self):
        pyrosim.Start_URDF("body.urdf")
        bodySize = [self.length,self.width,self.width]
        pyrosim.Send_Cube(name="Head", pos=[0, 0, 1], size=bodySize, colorName='<material name="Green">',
                          rgba='    <color rgba="0 1.0 0 1.0"/>')
        pyrosim.Send_Joint(name="Head_Body0", parent="Head", child="Body0", type="revolute", jointAxis="0 1 0"
                           , position=[bodySize[0]/-2, 0, 1])
        for i in range(c.numLinks):
            linkSize = [self.length,self.width,self.width]
            pyrosim.Send_Cube(name=f"Body{i}", pos=[linkSize[0]/-2, 0, 0], size=linkSize,
                              colorName='<material name="Green">',
                              rgba='    <color rgba="0 1.0 0 1.0"/>')
            if i+1 < c.numLinks:
                pyrosim.Send_Joint(name=f"Body{i}_Body{i+1}",parent=f"Body{i}", child=f"Body{i+1}",
                               type="revolute",jointAxis="0 1 0",position=[linkSize[0]*-1,0,0])

        pyrosim.End()
    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")
        pyrosim.Send_Sensor_Neuron(name=0, linkName="Head")
        for i in range(c.numSensorNeurons):
            pyrosim.Send_Sensor_Neuron(name=i+1, linkName=f"Body{i}")
        pyrosim.Send_Motor_Neuron(name=c.numSensorNeurons, jointName="Head_Body0")
        for i in range(c.numMotorNeurons):
            pyrosim.Send_Motor_Neuron(name=c.numSensorNeurons+i+1, jointName=f"Body{i}_Body{i+1}")

        for currentRow in range(0, c.numSensorNeurons):
            for currentColumn in range(0,c.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName=currentRow, targetNeuronName=currentColumn+c.numSensorNeurons,
                                     weight=self.weights[currentRow, currentColumn])

        pyrosim.End()

    def Set_ID(self, ID):
        self.myID = ID