import os
from parallelhillclimber import PARALLEL_HILL_CLIMBER
import numpy as np

"""
for i in range(5):
    os.system("python3 generate.py")
    os.system("python3 simulate.py")
"""
seed = int(input("enter seed:" ))
phc = PARALLEL_HILL_CLIMBER(seed)
phc.Evolve()
phc.Save_Data()
input("press enter to continue:" )
phc.Show_Best()


