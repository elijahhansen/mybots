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
        os.system(f"python3 simulate.py {directOrGUI} {self.myID} &")

    def Wait_For_Simulation_To_End(self):
        while not os.path.exists(f"fitness{self.myID}.txt"):
            t.sleep(0.01)
        f = open(f"fitness{self.myID}.txt", "r")
        self.fitness = float(f.read())
        f.close()
        os.system(f"rm fitness{self.myID}.txt")

    def Mutate(self):
        randomRow = random.randint(0, c.numMotorNeurons)
        randomColumn = random.randint(0, 1)
        self.weights[randomRow, randomColumn] = random.random() * c.numMotorNeurons - 1



    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[self.x + 3, self.y + 3, self.z], size=[self.length, self.width, self.height])
        pyrosim.End()

    def Create_Body(self):
        pyrosim.Start_URDF("body.urdf")
        pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1], size=[self.length, self.width, self.height])
        pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute",
                           position=[0, -0.5, 1],jointAxis="1 0 0")
        pyrosim.Send_Cube(name="BackLeg", pos=[0, -0.5, 0], size=[self.length-.8, self.width, self.height-.8])
        pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute",
                           position=[0, 0.5, 1],jointAxis="1 0 0")
        pyrosim.Send_Cube(name="FrontLeg", pos=[0, 0.5, 0], size=[self.length-.8, self.width, self.height-.8])
        pyrosim.Send_Cube(name="LeftLeg", pos=[-.5,0,0], size=[self.length, self.width-.8,self.height-.8])
        pyrosim.Send_Joint(name="Torso_LeftLeg", parent="Torso", child="LeftLeg", type="revolute",
                           position=[-.5,0,1],jointAxis="0 1 0")
        pyrosim.Send_Cube(name="RightLeg", pos=[.5, 0, 0], size=[self.length, self.width - .8, self.height - .8])
        pyrosim.Send_Joint(name="Torso_RightLeg", parent="Torso", child="RightLeg", type="revolute",
                           position=[.5, 0, 1], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="FrontLowerLeg", pos=[0, 0, -.5], size=[self.length-.8, self.width - .8, self.height])
        pyrosim.Send_Joint(name="FrontLeg_FrontLowerLeg", parent="FrontLeg", child="FrontLowerLeg", type="revolute",
                           position=[0, 1, 0], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="BackLowerLeg", pos=[0, 0, -0.5], size=[self.length - .8, self.width - .8, self.height])
        pyrosim.Send_Joint(name="BackLeg_BackLowerLeg", parent="BackLeg", child="BackLowerLeg", type="revolute",
                           position=[0, -1, 0], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="LeftLowerLeg", pos=[0, 0, -0.5], size=[self.length - .8, self.width - .8, self.height])
        pyrosim.Send_Joint(name="LeftLeg_LeftLowerLeg", parent="LeftLeg", child="LeftLowerLeg", type="revolute",
                           position=[-1, 0, 0], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="RightLowerLeg", pos=[0, 0, -.5], size=[self.length - .8, self.width - .8, self.height])
        pyrosim.Send_Joint(name="RightLeg_RightLowerLeg", parent="RightLeg", child="RightLowerLeg", type="revolute",
                           position=[1, 0, 0], jointAxis="0 1 0")

        pyrosim.End()
    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")
        pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
        pyrosim.Send_Sensor_Neuron(name=1, linkName="BackLeg")
        pyrosim.Send_Sensor_Neuron(name=2, linkName="FrontLeg")
        pyrosim.Send_Sensor_Neuron(name=3, linkName="LeftLeg")
        pyrosim.Send_Sensor_Neuron(name=4, linkName="RightLeg")
        pyrosim.Send_Sensor_Neuron(name=5, linkName="FrontLowerLeg")
        pyrosim.Send_Sensor_Neuron(name=6, linkName="BackLowerLeg")
        pyrosim.Send_Sensor_Neuron(name=7, linkName="LeftLowerLeg")
        pyrosim.Send_Sensor_Neuron(name=8, linkName="RightLowerLeg")
        pyrosim.Send_Motor_Neuron(name=9, jointName="Torso_BackLeg")
        pyrosim.Send_Motor_Neuron(name=10, jointName="Torso_FrontLeg")
        pyrosim.Send_Motor_Neuron(name=11, jointName="Torso_LeftLeg")
        pyrosim.Send_Motor_Neuron(name=12, jointName="Torso_RightLeg")
        pyrosim.Send_Motor_Neuron(name=13, jointName="FrontLeg_FrontLowerLeg")
        pyrosim.Send_Motor_Neuron(name=14, jointName="BackLeg_BackLowerLeg")
        pyrosim.Send_Motor_Neuron(name=15, jointName="LeftLeg_LeftLowerLeg")
        pyrosim.Send_Motor_Neuron(name=16, jointName="RightLeg_RightLowerLeg")
        pyrosim.Send_Synapse(sourceNeuronName=0, targetNeuronName=3, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=3, targetNeuronName=9, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=3, targetNeuronName=10, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=3, targetNeuronName=11, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=3, targetNeuronName=12, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=4, targetNeuronName=12, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=5, targetNeuronName=14, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=7, targetNeuronName=16, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=6, targetNeuronName=13, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=9, targetNeuronName=10, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=8, targetNeuronName=11, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=1, targetNeuronName=4, weight=10.0)
        ##pyrosim.Send_Synapse(sourceNeuronName=2, targetNeuronName=3, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=2, targetNeuronName=4, weight=10.0)
        ##pyrosim.Send_Synapse(sourceNeuronName=1, targetNeuronName=4, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=0, targetNeuronName=4, weight=10.0)
        for currentRow in range(0, c.numSensorNeurons):
            for currentColumn in range(0,c.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName=currentRow, targetNeuronName=currentColumn+c.numSensorNeurons,
                                     weight=self.weights[currentRow, currentColumn])

        pyrosim.End()

    def Set_ID(self, ID):
        self.myID = ID