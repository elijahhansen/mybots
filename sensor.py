import pyrosim.pyrosim as pyrosim
import numpy as np
import time as t

class SENSOR:
    def __init__(self, linkName):
        self.linkName = linkName
        self.values = np.zeros(10000)

    def get_value(self, i):
        self.values[i] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)

    def save_values(self):
        np.save('data/sensorvalues.npy',self.values)
