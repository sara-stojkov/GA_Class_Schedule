# Genetic Algorithm applied to making a College Schedule

## Authors: Sara Stojkov & Marko Milutin

## The task
Implementing a genetic algorithm in Python to create a timetable for university lectures and exercises. Each event must be assigned a day, time, and classroom, following these constraints:

- A minimum 15-minute break between events in the same classroom

- Classes run only from 7:00 AM to 7:00 PM, Monday to Friday

The goal is to maximize the product of the average idle times before the first and after the last event for each classroom and day. Input data is provided in _data_timetable.txt_. No GUI is provided, all debugging happens in the terminal.

The project contains its documentation in the ```docs``` folder. It describes the program structure, problem constraints, mutation and crossover operators, selection strategy, parameter choices, and algorithm results.

## Implementation

1. The Population

An individual is a potential solution to a problem - in this case a Schedule. Here, a Schedule is implemented as a list where a list element is actually a timeslot of 15 minutes on a specific workday in a specific classroom. A population is implemented as just a list of individuals (Schedules). Creating the first generation is done by adding classes to random slots in a Schedule's _class_list_, while taking into account that a class should be within 1 block - 1 block is a combination of a day and a classroom.

2. Fitness function
   
Fitness is calculated in two steps: the first step is a check if a schedule is valid - a valid schedule cannot have overlaps and it also has to have 15 minute breaks (1 timeslot) between activities in the same classroom. The second part of the fitness function checks how early the classes start and how late they end - the function we want to maximize. 

3. Crossovers

The selection of parents is implemented as a roulette selection - individuals are ranked by their fitness scores. A list with random numbers between 0 and 1 is generated and then the final score is a product of their fitness rank and the random number with their index from the second list. The individuals are sorted by those final scores and two with the biggest scores are selected to be the parents. 

The crossover function is implemented like a three-way crossover. Two points are chosen and the children are a combination of three segments that those two points make in the parents. 

  
4. Mutations

After new individuals are created in crossover, they are subject to mutations. There is a parameter ```MUTATION_CHANCE``` that determines how likely the mutations are to happen. In this implementation, there is variable chance to mutate - in the first half of generations, mutations are more likely to happen since they increase diversity. Mutations are also random, since they may shuffle from 1/16 classes to 1/4 of the general number of classes in a Schedule. A class is replaced by chosing a new random spot and removing the class from the old index.

5. Selection

THe choice of which individuals survive and build the next generation is done by using elitism. A parameter ```KEEP_PERCENT``` is defined to state how much of the parent generation is kept. Only the individuals with best fitness scores survive to next generations. The rest of the population is filled with children Schedules with thw best scores. This is done to avoid local minimums and stagnation.

## Results and an example schedule

The results of the algortihm are explained in detail in the documentation, but here is and example of how a part of one workday looks:

<img width="1900" height="768" alt="image" src="https://github.com/user-attachments/assets/6a9b0009-4cd4-4d6c-aa6d-43d312d15844" />
