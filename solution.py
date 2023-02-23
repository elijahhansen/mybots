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
        self.weights = np.random.rand(c.numSensorNeurons, c.numMotorNeurons)
        self.weights = self.weights * c.numMotorNeurons - 1
        self.x = 0
        self.y = 0
        self.z = 0.5
        self.length = 1
        self.width = 1
        self.height = 1
        self.plan = PLAN()
        self.get_plan = self.plan.Get_Plan()
        self.boolArray = self.plan.boolArray
        self.links = self.get_plan[0]
        self.joints = self.get_plan[1]

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
        #pyrosim.Send_Cube(name="Box", pos=[self.x - 3, self.y - 3, self.z], size=[self.length, 100, self.height],mass=0)
        pyrosim.End()

    def Create_Body(self):
        pyrosim.Start_URDF("body.urdf")
        links = self.links
        joints = self.joints
        print(links)
        print(joints)
        pyrosim.Send_Cube(name=links[0].name, pos=links[0].abspos,size=links[0].size,colorName=links[0].colorName,
                          rgba=links[0].rgba)
        pyrosim.Send_Joint(name=joints[0].name,parent=joints[0].parent,child=joints[0].child,type=joints[0].jointtype,
                           position=joints[0].position, jointAxis=joints[0].axis)
        for link in links:
            print(link.name)
            pyrosim.Send_Cube(name=link.name, pos=link.relativepos,size=link.size,
                              colorName=link.colorName,rgba=link.rgba)
        for joint in joints:
            print(joint.name)
            pyrosim.Send_Joint(name=joint.name, parent=joint.parent, child=joint.child,
                               type=joint.jointtype,position=joint.position, jointAxis=joint.axis)
        pyrosim.End()
    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")
        count = 0
        if self.boolArray[0] == 1:
            pyrosim.Send_Sensor_Neuron(name=count, linkName="Head")
            print(count, "Head")
            count += 1
        for i in range(c.numLinks):
            if self.boolArray[i+1] == 1:
                pyrosim.Send_Sensor_Neuron(name=count, linkName=f"Body{i}")
                print(count, f"Body{i}")
                count +=1
        print("end of sensors")
        sensor_count = count
        pyrosim.Send_Motor_Neuron(name=count, jointName="Head_Body0")
        print(count)
        count += 1
        for i in range(c.numLinks-1):
            pyrosim.Send_Motor_Neuron(name=count, jointName=f"Body{i}_Body{i+1}")
            print(count, f"Body{i}_Body{i+1}")
            count += 1
        for currentRow in range(sensor_count):
            for currentColumn in range(count-sensor_count-1):
                pyrosim.Send_Synapse(sourceNeuronName=currentRow, targetNeuronName=currentColumn+sensor_count-1,
                                     weight=self.weights[currentRow, currentColumn])

        pyrosim.End()

    def Set_ID(self, ID):
        self.myID = ID