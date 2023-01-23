import pybullet as p
import pyrosim.pyrosim as pyrosim
import pybullet_data
from world import WORLD
from robot import ROBOT
from sensor import SENSOR
from motor import MOTOR
import time as t
import numpy as np



class SIMULATION:
    def __init__(self):
        self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        self.world = WORLD()
        self.robot = ROBOT()
        p.setGravity(0, 0, -9.8)
        self.robotId = self.robot.robotId
        ##pyrosim.Prepare_To_Simulate(self.robotId)


    def run(self):
        for i in range(0, 1000):
            p.stepSimulation()
            self.robot.sense(i)
            self.robot.think()
            self.robot.act()
            t.sleep(1 / 2400)
    ##self.sensor.save_values()
    ##self.motor.save_values()

            """
           
            pyrosim.Set_Motor_For_Joint(bodyIndex=robotId, jointName=b'Torso_BackLeg', controlMode=p.POSITION_CONTROL,
                                        targetPosition=TargetAnglesBack[i], maxForce=80)
            pyrosim.Set_Motor_For_Joint(bodyIndex=robotId, jointName=b'Torso_FrontLeg', controlMode=p.POSITION_CONTROL,
                                        targetPosition=TargetAnglesFront[i], maxForce=80)
            """
    def __del__(self):
        p.disconnect()

