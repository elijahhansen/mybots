from solution import SOLUTION
import constants as c
import copy
import os
import copy
import numpy as np
import matplotlib.pyplot as mpl
import pickle


class PARALLEL_HILL_CLIMBER:
    def __init__(self,seed):
        os.system("rm brain*.nndf")
        os.system("rm fitness*.txt")
        os.system("rm body*.urdf")
        self.parents = {}
        self.nextAvailableID = 0
        self.seed = seed
        np.random.seed(self.seed)
        os.system(f"rm pickles/run{self.seed}.pkl")
        for i in range(c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1

        self.fitnessList = np.zeros((c.populationSize, c.numberOfGenerations + 1))
        #self.parent = SOLUTION()

    def Evolve(self):
        self.Evaluate(self.parents)
        for member in range(c.populationSize):
            self.fitnessList[member][0] = self.parents[member].fitness

        for currentGeneration in range(c.numberOfGenerations):
            print(f"Generation: #{currentGeneration}")
            self.Evolve_For_One_Generation()
            for member in range(c.populationSize):
                self.fitnessList[member][currentGeneration + 1] = self.parents[member].fitness

    def Save_Data(self):
        for i in range(c.populationSize):
            for j in range(c.numberOfGenerations + 1):
                self.fitnessList[i][j] *= -1
                if self.fitnessList[i][j] < 0:
                    self.fitnessList[i][j] = 0

        np.save(f"data/fitnessValues{self.seed}.npy", self.fitnessList)

        for i in range(len(self.fitnessList)):
            mpl.plot(self.fitnessList[i], label=f"member #{i + 1}")
            mpl.title(f"Fitness Across {c.numberOfGenerations} Generations, Seed #{self.seed}")
            mpl.xlabel("Number of Generations")
            mpl.ylabel("Fitness")
        # matplotlib.pyplot.legend()
        mpl.savefig(f"graphs/fitness{self.seed}.png", format="png")


    def Evolve_For_One_Generation(self):
        self.Spawn()

        self.Mutate()

        self.Evaluate(self.children)

        self.Print()

        self.Select()


    def Spawn(self):
        self.children = {}
        for parent in self.parents:
            self.children[parent] = copy.deepcopy(self.parents[parent])
            self.children[parent].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1

    def Mutate(self):
        for child in self.children:
            self.children[child].Mutate()


    def Select(self):
        for key in self.parents:
            if self.children[key].fitness < self.parents[key].fitness:
                self.parents[key] = self.children[key]

    def Print(self):
        for key in self.parents:
            print("parent:",self.parents[key].fitness, "child:", self.children[key].fitness)

    def Show_Best(self):
        solution = self.parents[0]
        for key in self.parents:
            if self.parents[key].fitness < solution.fitness:
                solution = self.parents[key]

        print("best:",solution.fitness)

        pickle.dump(solution, open(f"pickles/run{self.seed}.pkl", "wb"))
        solution.Start_Simulation("GUI")

        #self.parent.Evaluate("GUI")

    def Evaluate(self, solutions):
        for key in solutions:
            solutions[key].Start_Simulation("DIRECT")
        for key in solutions:
            solutions[key].Wait_For_Simulation_To_End()
