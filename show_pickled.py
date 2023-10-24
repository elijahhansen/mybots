from solution import SOLUTION
import sys
import pickle
seed = int(sys.argv[1])

try:
    solution = pickle.load(open(f"pickles/run{seed}.pkl", "rb"))
    solution.Start_Simulation("GUI")
except ValueError:
    print("invalid seed number: try an integer from 0 to 9")