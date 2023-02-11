from solution import SOLUTION
import constants as c
import copy
import os
import copy


class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        os.system("rm brain*.nndf")
        os.system("rm fitness*.txt")
        self.parents = {}
        self.nextAvailableID = 0
        for i in range(c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1
        #self.parent = SOLUTION()

    def Evolve(self):
        self.Evaluate(self.parents)

        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation()


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
            print()
            print("parent:",self.parents[key].fitness, "child:", self.children[key].fitness)
            print()

    def Show_Best(self):
        solution = self.parents[0]
        for key in self.parents:
            if self.parents[key].fitness < solution.fitness:
                solution = self.parents[key]

        print("best:",solution.fitness)
        solution.Start_Simulation("GUI")

        #self.parent.Evaluate("GUI")

    def Evaluate(self, solutions):
        for key in solutions:
            solutions[key].Start_Simulation("DIRECT")
        for key in solutions:
            solutions[key].Wait_For_Simulation_To_End()
