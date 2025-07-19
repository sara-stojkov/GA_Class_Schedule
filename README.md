# Genetic Algorithm applied to making a College Schedule

## Authors: Sara Stojkov & Marko Milutin

## Overview

Implementing a genetic algorithm in Python to create a timetable for university lectures and exercises. Each event must be assigned a day, time, and classroom, following these constraints:

- A minimum 15-minute break between events in the same classroom

- Classes run only from 7:00 AM to 7:00 PM, Monday to Friday

The goal is to **maximize the product of the average idle times before the first and after the last event for each classroom and day**. Input data is provided in _data_timetable.txt_. 

No GUI is implemented but the final schedule is saved as a HTML file which containts the Schedule day by day and room by room. 

Also, the documentation of the project is in the _docs_ folder describing the program structure, problem constraints, mutation and crossover operators, selection strategy, parameter choices, and algorithm results.

## Implementation

1. An individual

An individual in our genetic algorithm is actually a Schedule - a possible solution. A schedule is realised my making a matrix (list of lists), where the small list is actually a timeslot in a specific classroom and on a specific weekday. This implementation also includes a dictionary named mapping which has the starting index of each class to avoid unneccessary for loops and iterating through all timeslots.
A population is just a list of Schedules (a group of individuals).

2. Fitness Function

Fitness is calculated as ```points / penalty``` where points are earned when a Schedule follows the desirable traits - like if it has pauses between classes and starts later than 7 AM. Penalties are earned if a Schedule has overlapping classes or has no 15 minute pauses between classes.  

3. Mutations

Mutations randomize a variable number of classes within 1 block. A block is a combination of a classroom and a day - our logic does not allow a class spanning over blocks (like in real life).

4. Crossovers

Parents are chosen with roulette selection to prioritize better individuals but still allow for some randomness. A crossover is done using 3-way inheritance. 2 random spots (indexes in the parents' class lists) are chosen so they split each parents classes into 3 segments. The children are made by combining those segments like 1-2-1 and 2-1-2. In case of overlap, there is a chance a child may be more similar to a parent.

5. Selection

Elitism is used to allow only select few old individuals to move on to the next generation, while the rest of population is filled with children Schedules.

## Results and final schedule

The results of the algortihm are explained in detail in the documentation, but here is and example of how a part of one workday looks:

<img width="1900" height="768" alt="image" src="https://github.com/user-attachments/assets/6a9b0009-4cd4-4d6c-aa6d-43d312d15844" />

