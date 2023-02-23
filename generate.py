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
links, joints = plan.Get_Plan()
boolArray = plan.boolArray
weights = np.random.rand(c.numLinks+1, c.numLinks)
weights = weights * c.numLinks - 1


def create_world():
    pyrosim.Start_SDF("world.sdf")
    pyrosim.End()


create_world()


def Create_Body():
    pyrosim.Start_URDF("body.urdf")
    print(links)
    print(joints)
    pyrosim.Send_Cube(name=links[0].name, pos=links[0].abspos, size=links[0].size, colorName=links[0].colorName,
                      rgba=links[0].rgba)
    pyrosim.Send_Joint(name=joints[0].name, parent=joints[0].parent, child=joints[0].child, type=joints[0].jointtype,
                       position=joints[0].position, jointAxis=joints[0].axis)
    for i in range(1,len(links)):
        print(links[i].name)
        pyrosim.Send_Cube(name=links[i].name, pos=links[i].relativepos, size=links[i].size,
                          colorName=links[i].colorName, rgba=links[i].rgba)
    for j in range(1,len(joints)):
        print(joints[j].name)
        pyrosim.Send_Joint(name=joints[j].name, parent=joints[j].parent, child=joints[j].child,
                           type=joints[j].jointtype, position=joints[j].position, jointAxis=joints[j].axis)
    pyrosim.End()


def Create_Brain():
    pyrosim.Start_NeuralNetwork(f"brain{0}.nndf")
    count = 0
    if boolArray[0] == 1:
        pyrosim.Send_Sensor_Neuron(name=count, linkName="Head")
        print(count, "Head")
        count += 1
    for i in range(c.numLinks):
        if boolArray[i + 1] == 1:
            pyrosim.Send_Sensor_Neuron(name=count, linkName=f"Body{i}")
            print(count, f"Body{i}")
            count += 1
    print("end of sensors")
    sensor_count = count
    pyrosim.Send_Motor_Neuron(name=count, jointName="Head_Body0")
    print(count)
    count += 1
    for i in range(c.numLinks - 1):
        pyrosim.Send_Motor_Neuron(name=count, jointName=f"Body{i}_Body{i + 1}")
        print(count, f"Body{i}_Body{i + 1}")
        count += 1
    for currentRow in range(sensor_count):
        for currentColumn in range(count - sensor_count - 1):
            pyrosim.Send_Synapse(sourceNeuronName=currentRow, targetNeuronName=currentColumn + sensor_count - 1,
                                 weight=weights[currentRow, currentColumn])

    pyrosim.End()


Create_Body()
Create_Brain()
