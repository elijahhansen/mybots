import pyrosim.pyrosim as pyrosim
import random
from plan import PLAN
import constants as c
import numpy as np
x = 0
y = 0
z = 0.5
length = 1
width = 1
height = 1
plan = PLAN()
links, joints = plan.Make_Blueprint()
boolArray = plan.boolArray


def create_world():
    pyrosim.Start_SDF("world.sdf")
    pyrosim.End()


create_world()


def Create_Body():
    pyrosim.Start_URDF("body.urdf")
    print(links)
    print(joints)
    for i in range(len(links)):
        print(links[i].name)
        pyrosim.Send_Cube(name=links[i].name, pos=links[i].pos, size=links[i].size,
                          colorName=links[i].colorName, rgba=links[i].rgba)
    for j in range(len(joints)):
        print(joints[j].name)
        pyrosim.Send_Joint(name=joints[j].name, parent=joints[j].parent, child=joints[j].child,
                           type=joints[j].jointtype, position=joints[j].position, jointAxis=joints[j].axis)
    pyrosim.End()


def Create_Brain():
    pyrosim.Start_NeuralNetwork(f"brain{0}.nndf")
    count = 0
    for i in range(len(links)-1):
        if boolArray[i] == 1:
            pyrosim.Send_Sensor_Neuron(name=count, linkName=links[i].name)
            count += 1

    print("end of sensors")
    for j in range(len(joints)-1):
        pyrosim.Send_Motor_Neuron(name=count+j, jointName=joints[j].name)

    weights = np.random.rand(count, c.numMotorNeurons) * 2 - 1
    for currentRow in range(count):
        for currentColumn in range(c.numMotorNeurons):
            pyrosim.Send_Synapse(sourceNeuronName=currentRow, targetNeuronName=currentColumn + count,
                                 weight=weights[currentRow, currentColumn])
    pyrosim.End()


Create_Body()
Create_Brain()
