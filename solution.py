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
        randomRow = random.randint(0, c.numMotorNeurons)
        randomColumn = random.randint(0, 1)
        self.weights[randomRow, randomColumn] = random.random() * c.numMotorNeurons - 1



    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[self.x - 3, self.y - 3, self.z], size=[self.length, 100, self.height],mass=0)
        pyrosim.End()

    def Create_Body(self):
        pyrosim.Start_URDF("body.urdf")
        pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1], size=[self.length, self.width, self.height])
        pyrosim.Send_Cube(name="Hips", pos=[.5, 0, 0], size=[self.length, self.width, self.height])
        pyrosim.Send_Joint(name="Torso_Hips", parent="Torso", child="Hips", type="revolute",
                           position=[.7, 0, 1], jointAxis="0 0 1")
        pyrosim.Send_Cube(name="LeftHipsLeg", pos=[0, 0.5, 0], size=[self.length - .8, self.width, self.height - .8])
        pyrosim.Send_Joint(name="Hips_LeftHipsLeg", parent="Hips", child="LeftHipsLeg", type="revolute",
                           position=[0.5, 0.5, 0], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="LeftHipsLowerLeg", pos=[0, 0, -0.5], size=[self.length - .8, self.width - .8, self.height])
        pyrosim.Send_Joint(name="LeftHipsLeg_LeftHipsLowerLeg", parent="LeftHipsLeg", child="LeftHipsLowerLeg", type="revolute",
                           position=[0, 1, 0], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="RightHipsLeg", pos=[0, -0.5, 0], size=[self.length - .8, self.width, self.height - .8])
        pyrosim.Send_Joint(name="Hips_RightHipsLeg", parent="Hips", child="RightHipsLeg", type="revolute",
                           position=[0.5, -0.5, 0], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="RightHipsLowerLeg", pos=[0, 0, -.5], size=[self.length - .8, self.width - .8, self.height])
        pyrosim.Send_Joint(name="RightHipsLeg_RightHipsLowerLeg", parent="RightHipsLeg", child="RightHipsLowerLeg", type="revolute",
                           position=[0, -1, 0], jointAxis="0 1 0")

        pyrosim.Send_Cube(name="BackHipsLeg", pos=[.5, 0, 0], size=[self.length, self.width-.8, self.height - .8])
        pyrosim.Send_Joint(name="Hips_BackHipsLeg", parent="Hips", child="BackHipsLeg", type="revolute",
                           position=[1, 0, 0], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="BackHipsLowerLeg", pos=[0, 0, -.5], size=[self.length - .8, self.width - .8, self.height])
        pyrosim.Send_Joint(name="BackHipsLeg_BackHipsLowerLeg", parent="BackHipsLeg", child="BackHipsLowerLeg", type="revolute",
                           position=[1, 0, 0], jointAxis="0 1 0")
        pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute",
                           position=[0, -0.5, 1],jointAxis="1 0 0")
        pyrosim.Send_Cube(name="BackLeg", pos=[0, -0.5, 0], size=[self.length-.8, self.width, self.height-.8])
        pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute",
                           position=[0, 0.5, 1],jointAxis="1 0 0")
        pyrosim.Send_Cube(name="FrontLeg", pos=[0, 0.5, 0], size=[self.length-.8, self.width, self.height-.8])

        pyrosim.Send_Cube(name="LeftLeg", pos=[-.5,0,0], size=[self.length, self.width-.8,self.height-.8])
        pyrosim.Send_Joint(name="Torso_LeftLeg", parent="Torso", child="LeftLeg", type="revolute",
                           position=[-.5,0,1],jointAxis="0 1 0")
        """
        pyrosim.Send_Cube(name="RightLeg", pos=[.5, 0, 0], size=[self.length, self.width - .8, self.height - .8])
        pyrosim.Send_Joint(name="Torso_RightLeg", parent="Torso", child="RightLeg", type="revolute",
                           position=[.5, 0, 1], jointAxis="0 1 0")
        """
        pyrosim.Send_Cube(name="FrontLowerLeg", pos=[0, 0, -.5], size=[self.length-.8, self.width - .8, self.height])
        pyrosim.Send_Joint(name="FrontLeg_FrontLowerLeg", parent="FrontLeg", child="FrontLowerLeg", type="revolute",
                           position=[0, 1, 0], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="BackLowerLeg", pos=[0, 0, -.5], size=[self.length - .8, self.width - .8, self.height])
        pyrosim.Send_Joint(name="BackLeg_BackLowerLeg", parent="BackLeg", child="BackLowerLeg", type="revolute",
                           position=[0, -1, 0], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="LeftLowerLeg", pos=[0, 0, -0.5], size=[self.length - .8, self.width - .8, self.height])
        pyrosim.Send_Joint(name="LeftLeg_LeftLowerLeg", parent="LeftLeg", child="LeftLowerLeg", type="revolute",
                           position=[-1, 0, 0], jointAxis="0 1 0")
        """
        pyrosim.Send_Cube(name="RightLowerLeg", pos=[0, 0, -.5], size=[self.length - .8, self.width - .8, self.height])
        pyrosim.Send_Joint(name="RightLeg_RightLowerLeg", parent="RightLeg", child="RightLowerLeg", type="revolute",
                           position=[1, 0, 0], jointAxis="0 1 0")
                           """


        pyrosim.End()
    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")
        pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
        pyrosim.Send_Sensor_Neuron(name=1, linkName="Hips")
        pyrosim.Send_Sensor_Neuron(name=2, linkName="BackLeg")
        pyrosim.Send_Sensor_Neuron(name=3, linkName="LeftLeg")
        pyrosim.Send_Sensor_Neuron(name=4, linkName="FrontLeg")
        pyrosim.Send_Sensor_Neuron(name=5, linkName="BackHipsLeg")
        pyrosim.Send_Sensor_Neuron(name=6, linkName="LeftHipsLeg")
        pyrosim.Send_Sensor_Neuron(name=7, linkName="RightHipsLeg")
        pyrosim.Send_Sensor_Neuron(name=8, linkName="BackLowerLeg")
        pyrosim.Send_Sensor_Neuron(name=9, linkName="LeftLowerLeg")
        pyrosim.Send_Sensor_Neuron(name=10, linkName="BackHipsLowerLeg")
        pyrosim.Send_Sensor_Neuron(name=11, linkName="RightHipsLowerLeg")
        pyrosim.Send_Sensor_Neuron(name=12, linkName="LeftHipsLowerLeg")
        pyrosim.Send_Sensor_Neuron(name=13, linkName="FrontLowerLeg")
        pyrosim.Send_Motor_Neuron(name=14, jointName="Torso_BackLeg")
        pyrosim.Send_Motor_Neuron(name=15, jointName="Torso_Hips")
        pyrosim.Send_Motor_Neuron(name=16, jointName="Torso_LeftLeg")
        pyrosim.Send_Motor_Neuron(name=17, jointName="Torso_FrontLeg")
        pyrosim.Send_Motor_Neuron(name=18, jointName="Hips_BackHipsLeg")
        pyrosim.Send_Motor_Neuron(name=19, jointName="Hips_LeftHipsLeg")
        pyrosim.Send_Motor_Neuron(name=20, jointName="Hips_RightHipsLeg")
        pyrosim.Send_Motor_Neuron(name=21, jointName="BackLeg_BackLowerLeg")
        pyrosim.Send_Motor_Neuron(name=22, jointName="LeftLeg_LeftLowerLeg")
        pyrosim.Send_Motor_Neuron(name=23, jointName="FrontLeg_FrontLowerLeg")
        pyrosim.Send_Motor_Neuron(name=24, jointName="BackHipsLeg_BackHipsLowerLeg")
        pyrosim.Send_Motor_Neuron(name=25, jointName="LeftHipsLeg_LeftHipsLowerLeg")
        pyrosim.Send_Motor_Neuron(name=26, jointName="RightHipsLeg_RightHipsLowerLeg")
        """
        pyrosim.Send_Synapse(sourceNeuronName=0, targetNeuronName=16, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=0, targetNeuronName=17, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=0, targetNeuronName=19, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=0, targetNeuronName=18, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=0, targetNeuronName=24, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=0, targetNeuronName=23, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=0, targetNeuronName=25, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=0, targetNeuronName=27, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=1, targetNeuronName=18, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=1, targetNeuronName=19, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=1, targetNeuronName=20, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=1, targetNeuronName=22, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=2, targetNeuronName=17, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=2, targetNeuronName=16, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=2, targetNeuronName=19, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=2, targetNeuronName=20, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=3, targetNeuronName=19, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=3, targetNeuronName=17, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=3, targetNeuronName=23, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=3, targetNeuronName=22, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=3, targetNeuronName=26, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=3, targetNeuronName=27, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=4, targetNeuronName=18, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=4, targetNeuronName=19, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=4, targetNeuronName=20, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=4, targetNeuronName=21, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=4, targetNeuronName=26, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=4, targetNeuronName=27, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=5, targetNeuronName=16, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=5, targetNeuronName=17, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=5, targetNeuronName=18, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=5, targetNeuronName=19, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=5, targetNeuronName=20, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=5, targetNeuronName=21, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=5, targetNeuronName=23, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=6, targetNeuronName=16, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=6, targetNeuronName=17, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=6, targetNeuronName=18, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=6, targetNeuronName=19, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=6, targetNeuronName=21, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=6, targetNeuronName=24, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=6, targetNeuronName=25, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=6, targetNeuronName=27, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=7, targetNeuronName=16, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=7, targetNeuronName=17, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=7, targetNeuronName=18, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=7, targetNeuronName=19, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=7, targetNeuronName=21, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=7, targetNeuronName=24, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=7, targetNeuronName=25, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=7, targetNeuronName=27, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=8, targetNeuronName=16, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=8, targetNeuronName=17, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=8, targetNeuronName=18, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=8, targetNeuronName=19, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=8, targetNeuronName=21, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=8, targetNeuronName=24, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=8, targetNeuronName=25, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=8, targetNeuronName=27, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=9, targetNeuronName=16, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=9, targetNeuronName=17, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=9, targetNeuronName=18, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=9, targetNeuronName=19, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=9, targetNeuronName=21, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=9, targetNeuronName=24, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=9, targetNeuronName=25, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=9, targetNeuronName=27, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=10, targetNeuronName=16, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=10, targetNeuronName=17, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=10, targetNeuronName=18, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=10, targetNeuronName=19, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=10, targetNeuronName=21, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=10, targetNeuronName=24, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=10, targetNeuronName=25, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=10, targetNeuronName=27, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=12, targetNeuronName=16, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=12, targetNeuronName=17, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=12, targetNeuronName=18, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=12, targetNeuronName=19, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=11, targetNeuronName=21, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=11, targetNeuronName=24, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=11, targetNeuronName=25, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=13, targetNeuronName=27, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=13, targetNeuronName=21, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=13, targetNeuronName=24, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=13, targetNeuronName=25, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=13, targetNeuronName=27, weight=10.0)

        pyrosim.Send_Synapse(sourceNeuronName=10, targetNeuronName=26, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=11, targetNeuronName=26, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=12, targetNeuronName=26, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=13, targetNeuronName=26, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=6, targetNeuronName=26, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=7, targetNeuronName=26, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=8, targetNeuronName=26, weight=10.0)
        pyrosim.Send_Synapse(sourceNeuronName=9, targetNeuronName=26, weight=10.0)
        """

        for currentRow in range(0, c.numSensorNeurons):
            for currentColumn in range(0,c.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName=currentRow, targetNeuronName=currentColumn+c.numSensorNeurons,
                                     weight=self.weights[currentRow, currentColumn])

        pyrosim.End()

    def Set_ID(self, ID):
        self.myID = ID