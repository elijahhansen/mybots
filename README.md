# mybots
ludobots rep

# Ideas
The idea behind this project is to expand upon the existing 3D creatures codebase for evolution. The goal is to implement a mutation method that can randomly change the body and brain and ensure the positioning of the links/joints of the creatures stay intact. The creature's fitness function is the negative x direction, so the most fit creature will travel the farthest in the negative x direction. The evolutionary algorithm will run for a population of 50 creatures over 50 generations to ensure genetic diversity and proper evolution of the bodies and brain.

# Methods
The body was mutated by choosing a dimension to alter in each link of the creature and setting that dimension to a random size. If a link was mutated then the method also ensures that any change in size is met with appropriate changes to the relative positions of the link and any joints around it along with the absolute positions of the creature's links. I also implemented a tier system to the mutation method that decreased the randomness of the mutation when fitness thresholds were met. For example, when the creature evolved past fitness 3 the probability of size mutation decreased by 50% to ensure that smaller changes would occur. The brain is mutated by choosing a random synpase to alter and changing its weight to a random value and continues mutation after every fitness threshold.

# Instructions
Download the files and run "python3 search.py" in the terminal. Then you will be prompted to enter a seed integer for the random number generator the evolutionary algorithm will run over 50 generations and at the end show the most fit creature after asked to press enter/return. There will also be a fitness graph availible at graphs/fitness{seed}.png

# Images
![Notability Notes 2-1](https://user-images.githubusercontent.com/98726413/221771601-029c5006-a9bb-4147-af74-5f2dac5c7f74.png)

Visuals for Body Mutation

# Citations
Ludobots MOOC, Dr. Josh Bongard
Karl Sims
Pyrosim
PyBullet
