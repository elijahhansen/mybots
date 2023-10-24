import numpy as np
import matplotlib.pyplot as mpl
import constants as c

fitnessValues = []
bestVals = []
for i in range(10):
    fitnessValues.append(np.load(f"data/fitnessValues{i}.npy"))
    bestArray = []
    for k in range(c.numberOfGenerations+1):
        best = 0
        for j in range(c.populationSize):
            if fitnessValues[i][j][k] > fitnessValues[i][best][k]:
                best = j

        bestArray.append(fitnessValues[i][best][k])
    bestVals.append(bestArray)

for i in range(len(bestVals)):
    mpl.plot(bestVals[i], label=f"Seed #{i}")
mpl.title(f"Best Fitness Over {c.numberOfGenerations} Generations")
mpl.xlabel("Number of Generations")
mpl.ylabel("Fitness")
mpl.savefig("graphs/bestFitness.png", format="png")



