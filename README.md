# mybots
ludobots rep

# Ideas
The idea behind this project is to expand upon the existing 3D creatures codebase for evolution. The goal is to implement a mutation method that can randomly change the body and brain and ensure the positioning of the links/joints of the creatures stay intact. The creature's fitness function is the negative x direction, so the most fit creature will travel the farthest in the negative x direction. The evolutionary algorithm will run for a population of 50 creatures over 50 generations.

# Methods
The body was mutated by choosing a dimension to alter in each link of the creature and setting that dimension to a random size. If a link was mutated then the method also ensures that any change in size is met with appropriate changes to the relative positions of the link and any joints around it along with the absolute positions of the creature's links. The brain is mutated by choosing a random synpase to alter and changing its weight to a random value.

# Instructions
Download the files and run "python3 search.py" in the terminal and the evolutionary algorithm will over 50 generations and at the end show the most fit creature. There will also be a fitness graph availible at graphs/fitness.png

# Citations
Ludobots MOOC, Dr. Josh Bongard
Karl Sims
Pyrosim
PyBullet
