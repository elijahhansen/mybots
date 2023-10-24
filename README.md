# mybots
Evolved 3D Creatures by Elijah Hansen

![ezgif com-resize](https://user-images.githubusercontent.com/98726413/225178044-6b2971c1-b814-4de5-b955-9aa5e29eee24.gif)

# Summary Video
https://youtu.be/kDumBztHQlQ

# Main Idea
The idea behind this project is to expand upon the my existing 3D creatures codebase for evolution. The goal is to implement mutation methods that can randomly change the body and brain and ensure the positioning of the links/joints of the creatures stay intact and evolve to be fit creatures. The creature's fitness function is the negative x direction, so the most fit creature will travel the farthest in the negative x direction. The parallel hill climber was the evolutionary algoritm used in this project which takes each parent of the population, in this case 10 parents, mutates each one, evaluates whether the resulting child is more fit and select's the better of the parent/child pair. The evolutionary algorithm will run for a population of 10 creatures over 500 generations over 10 seeds to numpy's random number generator (50,000 simulations) to ensure both genetic diversity and proper evolution of the bodies and brain. Genetic diversity is very important in evolution because population need variety and random mutations to ensure progress over time.

# Methods
## Generation of Bodies
As shown below in Figure 1, the body is generated starting from a base link connected by a joint on a random face of the base link to a second link. From there the bodyplan algorithm chooses a random link and a random face and then connects a randomly sized link to the chosen face. This process will continue until there are no more links to connect (limited by a constant chosen by the user in `constants.py`). The genotype in this case are the lists of `LINK` and `JOINT` objects that will later be read in `solution.py` and sent to pyrosim, the simulator GUI. There the user can see the phenotype of the body plan. This acts like a blueprint and construction system.
## Generation of Brain
The brain is a fully connected neural network of sensor and motor neurons with random synapse weights. Because the network if fully connected, every sensor is connected to each motor. The neural network acts like a weighted directed graph with the neurons as nodes and the weights as the weight of each edge.
## Mutation of Bodies
The body was mutated by choosing a dimension to alter in each link of the creature and setting that dimension to a random size, as seen below in Figure 2. If a link was mutated then the method also ensures that any change in size is met with appropriate changes to the relative positions of the link and any joints around it along with the absolute positions of the creature's links. I also implemented a tier system to the mutation method that decreased the randomness of the mutation when fitness thresholds 3 and 6 were met. For example, when the creature evolved past fitness 3 the probability of size mutation decreased by 50% to ensure that smaller changes would occur. 
## Mutation of Brain
The brain is mutated by choosing a random synpase to alter and changing its weight to a random value between -1 and 1 and continues mutating after every fitness threshold; seen in Figure 3.
## Parallel Hill Climber
As described in the introduction to this project, the evolutionary algorithm used in this project is the parallel hill climber. This algorithm takes each parent, evolves them and compares each parent to their respective child. If the child is more fit than the parent then it replaces the parent for the next round of evolution. If not, then the parent does not change and moves on to the next generation. Once the generation count has been met (set by the user), the algorithm will go through each parent and find the one that is most fit and show that solution on screen.
## Functionality of Files
### constants.py
In the `constants.py` file the user is able to control a variety of factors relating to robot's characteristics and even the nature of the evolution of the robot. The user is able to control the number of links the robot will have, the frequency, phase offset, and and amplitude of the motors, the population size and number of generations for evolution, and the range of the joints.
### joint.py
* contains the `JOINT` class object used in formulating the body plan in `plan.py`
### links.py
* contains the `LINK` class object used in formulating the body plan in `plan.py`
* has method `Compute_Box()` which calculates the bounds of generation of the next body part to ensure no collisions in the body plan
### motor.py
* contains the `MOTOR` class object and sets motors for each joint in the body 
* here, the user can adjust the maxForce of a motor 
### parallelhillclimber.py
* houses the evolutionary algorithm of the robot
* here, the user can change anything about the process of evolution including the fitness function, how data is saved, and how to evaluate each robot
### plan.py
* this is where the blueprint is made for each random body
* the algoritm is described above: the plan generates links and the appropriate joints until the desired limit is reached
* collisions and any other 3D constraint for the body are handled in `Find_Collisions()`
* this file also handles any adjustments that need to be made to the body after mutations
### robot.py
* contains the `ROBOT` class object which sets up the robot's neural network and creates the `SENSOR` and `MOTOR` objects for the robot
* it also writes the fitness of each robot so that we can read it during evolution
### search.py
* acts like our main script
* requests the user to input a seed number and then runs `parallelhillclimber` and eventually shows the best robot
### sensor.py
* contains the `SENSOR` class object
* gets and saves sensor values 
### show_pickled.py
* by running `python3 show_pickled.py 0` the best robot from seed 0 will be shown
* run this file with any seed from 0-9 to see the pickled best robot from each run
### simulate.py
* calls `SIMULATION` methods and decides whether to run simulations in parallel or not
### simulation.py
* contains the `SIMULATION` class object which holds the methods for running the simulation on screen or directly without the GUI
* here, the user can modify the length of each run and how the simulations steps 
### solution.py
* contains the `SOLUTION` class object which holds methods for sending the body, brain, and world to the simulator
* here, the user can control which sensors get assigned and where, send world objects into scene, and modify how the body mutates 
### world.py
* contains the `WORLD` class object which simply loads the `plane.urdf` and `world.sdf` files

# Results
Compared to earlier versions of this projects, for example the `evolved_3D_creatures` project, the resulting bodies from evolution were a bit different. Of the 10 resulting bodies, a majority of them were wider than the creatures from `evolved_3D_creatures`. I attribute this to randomness because in this project only 10 parents were used each run and each generation only 1 link is mutated. Thus, I think it is by chance that the creatures took a wider form. I also found that a couple of the bodies were very similar to the previous iteration, which was run using 50 parents across 50 generations, which were Pixar lamp type creatures that hop. This design seems like a logical solution to me because it is very efficient. The design usually has only 3 or 4 links and a motor that keeps it bouncing in the negative x-direction. 

Additionally, I found that on some of the fitness graphs the fitness of the robots seemed to flatten out after reaching fitness 3; see the graph for seed 9 for am example (Figure 6). I infer that the tiered mutation system might have had unintended consequences related to the fitness of the robots. The goal of the tiered mutations was to decrease randomness of mutations when the robot was past fitness 3 and 6. However, since the progress flattened out I think that this decrease in probabilty of body mutation might have locked the robot in a local minima when the goal was to ensure this did not happen. However, in most runs I found that the creatures were not affected by this threshold system and actually benefitted from it. I infer this because in most graphs I see sharp increases in fitness followed by gradual improvements in fitness after fitness 3 and 6 that I attribute to tiered mutations.

I also found that the creatures sometimes grew to be too tall and hence kind of rolled to the finish line. I tried to account for this dilemma in my codebase by detecting a collision with an imaginary boundary at z=5 so that the creatures would not get too tall. However, some goofy robots still came from evolution and rolled like rollie pollies.


# Instructions
Download the files and run `python3 search.py` in the terminal. Then you will be prompted to enter a seed integer for the random number generator the evolutionary algorithm will run over 500 generations and at the end show the most fit creature after asked to press enter/return. There will also be a fitness graph availible at `graphs/fitness{seed}.png`. Additionally, after running seeds 0-9, running `python3 analyze.py` there will be a graph summarizing the fitness across each seed in the graphs directory.

# Figures
![bodies](https://user-images.githubusercontent.com/98726413/225148923-85be2f2c-e3f4-4d7f-b06e-7e7bb4a47cb0.png)
(Figure 1: Body Generation)

![Notability Notes (5)](https://user-images.githubusercontent.com/98726413/225149178-7d9b1a0c-a906-4323-abe6-962a7ebbb881.png)
(Figure 2: Body Mutation)

![Notability Notes (6)](https://user-images.githubusercontent.com/98726413/225149241-4763722f-1348-494d-88f7-d06cee9a71aa.png)
(Figure 3: Brain Mutation)

![bestFitness](https://user-images.githubusercontent.com/98726413/225163092-90530676-71ef-4921-acd1-2ed733580b60.png)
(Figure 4: Best Fitness)

![fitness0](https://user-images.githubusercontent.com/98726413/225204973-a11b7bc4-9950-45b0-bdc1-be125b24895c.png)
(Figure 5)

![fitness9](https://user-images.githubusercontent.com/98726413/225205015-35ff07a0-fb7d-4a04-b8d1-c6b63db3157b.png)
(Figure 6)


<img width="583" alt="Screen Shot 2023-02-28 at 1 28 20 AM" src="https://user-images.githubusercontent.com/98726413/221784567-98b96d1a-a56c-48d3-8141-bfe53ac73564.png">
Example creature (evolved)



# Citations
Ludobots MOOC, Dr. Josh Bongard
Karl Sims
Pyrosim
PyBullet
