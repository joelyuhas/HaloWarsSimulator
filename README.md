# HaloWarsSimulator

Experimental project that used Python to solve the problem of how quickly can a player create a "Scarab" super unit using the rules of the Halo Wars strategy game released in 2009.

Specifically, this project created a simulator that could accurately predict how many resources at a specific point in time a player would have based on the order their created bases and buildings. Then, a separate program created hundreds of thousands of random build orders that were simulated to find the fastest build order to 3000 resources.

This project used a significant amount of problem solving, software development, analysis, experimentation, and verification testing against in game experimentation. 

For a detailed technical analysis and breakdown of the project, design, findings, and discussion, see the PDF report saved in documents/Halo_Wars_Simulator_Report.pdf

## Objective

There were several objectives for this project the main ones being:
- Use Python to find the fastest way to build a Scarab Super Unit in Halo Wars
- Attempt to surpass the personal best time of 7 minutes, 10 seconds from before
- Use this project as an opportunity to practice advanced software development techniques and problem solving in Python
- Stretch goal of finding fastest time to build two Scarabs.

## High Level Overview
The Scarab is one of the most powerful units in the game Halo Wars. If the player can get one as fast as possible, it can provide them a major advantage.

The following is a very high level overview of the Halo Wars game mechanics and how the code was designed. For a technical, in-depth overview see the PDF in documents/Halo_Wars_Simulator_Report.pdf.

## Game Mechanics
### Actions
The player has several actions they can do that impact this project:
- Build/upgrade a base (creates more build slots for supply pads).
- Build/upgrade a supply pad (adds more resources per second).
- Build a Temple (adds a tech level).

Each mechanic costs a specific amount of resources and takes a certain amount of time. The more supply pads, the greater the supplies generated a second, but the greater up front cost.

### Scarab Requirements
To build a Scarab, the player needs:
- 3000 supplies.
- a Tech level of 3.

### Assumptions
This project assumed that the player was playing on the map "Exile", which has 4 "Reactors" on the map, which would let the player get a tech level of 3 after only building a Temple (assuming they can control 2).

### Economy
The player gets resources per second in a non-linear fashion based off the amount of regular supply pads, upgraded supply pads, and total supply pads. The exact equation and breakdown is discussed in the PDF.

## Software Design
Two main pieces of software were designed for this project, a program to simulate the Halo Wars in game economy and build times/constraints, and another to generate "Build Orders" to feed into the simulation.

### Simulator
The simulator used Python to replicate the Halo Wars mechanics as closely as possible. It did this by creating the following classes:
- Base Class: Controlled building bases and monitoring that bases build times and build slots.
- Build Slot Class: Controlled the building that was made on a base's build slot, could be empty, supply pad, or Temple.
- Resource Manager Class: Singleton class that handled all the resource calculations, tech levels, and other universal values.
- Runtime Building Blocks Class: Handled actually managing the classes and running the simulation by executing "build orders" and telling the Bases/Build Slots what to do and when.

All of this was wrapped in a SimulatorWrapper that could be easily interfaced with by the other program.

### Generating Build Orders
The second program also was done in Python and main purpose was to generate random "build orders", or a list of orders that simulator could act on.

At first statistics and combinatorics were attempted to get every build order possible, but that was deemed too challenging. Instead the it was thought of to generate random build orders, with the idea that even if it didn't find the fastest time, it could help show trends.

This class followed the rough overall flow:
- Generate a list to be used for build orders of a random length between 1 and max length.
- Using a probability cart, randomly select an order to do (build base, build supply pad, build Temple, etc).
- Build in safety mechanism ensured that the random order could be done, otherwise it would generate a new random order.
- A redundancy check using a hash map also was used to ensure no duplicate build orders were ran.


### Combining
A combination program was made that would create a random build order, simulate the build order, and save the output time it took the order to reach 3000 resources. This combination program would have several constants that could be toggled to change how many random iterations to run, what resource threshold to use, how many starting bases, etc.


## Results
Several experiments were ran, including calculating how long it took to reach 3000, 3300, and 6800 resources for one base and two base. 

The program found a significantly faster build order that built a scarab in 308 seconds, and also found very quick methods for building 2 Scarabs as well.

These build orders were tested on the actual Halo Wars game and were extremely accurate.

## Conclusion
The project was a massive success, it accomplished all of its goals and even stretch goals. The program found an incredibly fast build order, and the project was able to use many software development principals and provided many learning opportunities.

