# HaloWarsSimulator

Experimental project that used Python to figure out how quickly a player can create a "Scarab" super unit using the rules of the 2009 Halo Wars strategy game.

Specifically, in the game Halo Wars, "resoruces" are a currency the player uses to buy units. The player gets resrouces continuously based on how many buildings of a specific type they have. Since it takes resrouces and time to build buildings, the equation for calculating the fastest way to get to a certain number of resources is complex.

This project created a simulator that could accurately predict how many resources at a specific point in time a player would have based on the order they created their bases and buildings. A separate program created hundreds of thousands of random build orders that were simulated to find the fastest build order to reach the amount of resources it took to build a Scarab.

This project used a significant amount of problem solving, software development techniques, analysis, experimentation, and verification testing against in game experimentation. 

For a detailed technical analysis and breakdown of the project, design, findings, and discussion, see the PDF report saved in:
- documents/Halo_Wars_Simulator_Report.pdf

Originally created March 2024, report created Nov 2024.

## Objective

There were several objectives for this project, the main ones being:
- Use Python to find the fastest way to build a Scarab Super Unit in Halo Wars.
- Attempt to surpass the personal best time of 7 minutes, 10 seconds (430 seconds).
- Use this project as an opportunity to practice advanced software development techniques and problem solving in Python.
- Stretch goal of finding fastest time to build two Scarabs (6800 resources).

## High Level Overview
The following is a very high level overview of the Halo Wars game mechanics and how the code was designed. For a technical, in-depth overview see the PDF in documents/Halo_Wars_Simulator_Report.pdf.

The Scarab is one of the most powerful units in the game Halo Wars. If the player can get one as fast as possible, it can provide them a major advantage. The following are the game mechanics that show the rules this project needed to consider for how to build a Scarab.


### Game Mechanics
#### Scarab Requirements
To build a Scarab, the player needs the following requirements:
- 3000 resrouces.
- a Tech level of 3.


#### Actions
The player has several actions they can do that can help them satisfy the Scarab Requirements:
- Build/upgrade a base (creates more build slots for supply pads).
- Build/upgrade a supply pad (adds more resources per second).
- Build a Temple (adds a tech level).

Each mechanic costs a specific amount of resources and takes a certain amount of time to complete. The more supply pads, the greater the supplies generated a second is, but the greater up front cost.


#### Assumptions
This project assumed that the player was playing on a specific map which has 4 "Reactors", which are special abilities that let the player get a tech level of 3 after only building a Temple (assuming they can control 2 reactors).

#### Economy
The player gets resources per second in a non-linear fashion based off the amount of regular supply pads, upgraded supply pads, and total supply pads. The exact equation and breakdown is discussed in the PDF.

### Software Design
Two main pieces of software were designed for this project, a program to simulate the Halo Wars in game economy and build times/constraints, and another to generate "Build Orders" to feed into the simulatior.

#### Simulator
The simulator used Python to replicate the Halo Wars mechanics as closely as possible. It did this by creating the following classes:
- Base Class: Controlled building bases and monitoring that bases build times and build slots.
- Build Slot Class: Controlled the building that was made on a base's build slot, could be Empty, Supply Pad, or Temple.
- Resource Manager Class: Singleton class that handled all the resource calculations, tech levels, and other universal values.
- Runtime Building Blocks Class: Managed the classes and the running of the simulation by executing "build orders" and telling the Bases/Build Slots what to do and when.

All of this was wrapped in a SimulatorWrapper that could be easily interfaced with by the other program.

#### Generating Build Orders
The second program (GenerateOrdersBuildingBlocks) also was done in Python and main purpose was to generate random "build orders", or a list of orders that simulator could act on.

At first statistics and combinatorics were attempted to try to get every build order possible, but that was deemed too challenging. Instead, a method was used to generate random build orders, with the idea that even if it didn't find the fastest time, it could help show trends.

This class followed the overall flow:
- Generate a list to be used for build orders of a random length between 1 and a max length.
- Using a probability chart, randomly select an order (build base, build supply pad, build Temple, etc.).
- Built in safety mechanism ensured that the random order was valid, otherwise it would generate a new random order.
- A redundancy check using a hash map was used to ensure no duplicate build orders were ran.


#### Combining
A combination and executible program (run_build_combinations.py) was made that utilized both programs to create a random build order, simulate the build order, and save the output time it took the order to reach 3000 resources. This combination program would have several constants that could be toggled to change how many random iterations to run, what resource threshold to use, how many starting bases, etc.


## Results
Several experiments were run, including calculating how long it took to reach 3000, 3300, and 6800 resources for one base and two bases. 

The program found a significantly faster build order that built a scarab in 308 seconds vs the previously faster time of 430 seconds, and also found very quick methods for building 2 Scarabs.

These build orders were tested in the actual Halo Wars game and were extremely accurate.

## Conclusion
The project was a massive success, it accomplished all of its goals and even stretch goals. The program found an incredibly fast build order, and the project was able to use many software development principals and provided many learning opportunities.

