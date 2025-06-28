
from random import random, randint

from structures.subject import Subject

class Schedule:
    """
    Represents a schedule for classes in a school. It contains class_list, 
    it is a list of lists (each sublist represents a time slot so there are 12 hours * 4 quarters * 5 days  * room_count),
    so the first list is on Monday at 7:00 in the first room, the second is on Monday at 7:15 also first room, and so on.
    If the class lasts 1 hour, it will occupy 4 consecutive slots.
    Also, blocks are introduced to prevent overlap of one subject across days or different rooms.
    It is a list of lists, because in the beginning we allow multiple classes to be scheduled at the same time,
    but this will be corrected later in the algorithm (negative impact on fitness score).
    The mapping is a dictionary that maps class indices to their first positions (start of the class) in the class_list.

    """
    __slots__ = ('class_list', 'mapping', 'fitness_score', 'num_blocks', 'block_size')
    def __init__(self, class_count: int, room_count: int):
        # Initialize the schedule where the time slots are represented as a list of lists.
        # Each sublist corresponds to a time slot (12 hours * 4 quarters * 5 days * room_count).
        self.class_list = [[] for _ in range(12 * 4 * 5 * room_count)]
        # Initialize the mapping of classes to their indices.
        # The mapping is a dictionary where the key is the class index and the value is -1 (indicating no class scheduled).
        # The mapping will be updated when classes are added to the schedule.
        self.mapping = {i: -1 for i in range(class_count)}
        self.fitness_score = -1
        self.num_blocks = 5 * room_count  # We have 5 work days and n rooms, so each combination of these is one block
        self.block_size = 4 * 12 # Since we work with quarters of an hour, this is 4 quarters per 12 hours (from 7 am to 7 pm)

    def get_class_list(self):
        """Returns the list of classes in the schedule."""
        return self.class_list

    def get_mapping(self):
        """Returns the mapping of classes to their indices."""
        return self.mapping

    def get_fitness_score(self):
        """Returns the fitness score of the schedule."""
        return self.fitness_score

    def set_fitness_score(self, score: int) -> None:
        """Sets the fitness score of the schedule."""
        self.fitness_score = score

    def set_random_classes(self, room_number: int, classes: list[Subject]):
        """
        Used for randomizing an individual Schedule, used in creating the first generation.
        Iterates through all the classes and assignes them to a random timeslot (15 minutes) and classroom, according to Schedule structure. 
        Adding a class to the schedule is done by appending it to the class_list and updating the mapping.
        """

        class_number = len(classes)
        for i in range(class_number): # iterating through the indexes of all classes
            block_id = randint(0, self.num_blocks - 1) # first pick out a block
            block_start = block_id * self.block_size
            block_end = block_start + self.block_size - classes[i].duration

            random_class_index = randint(block_start, block_end)

            for j in range(classes[i].duration):
                    self.class_list[random_class_index + j].append(i) 
            self.mapping[i] = random_class_index 

        self.fitness(classes)


    def fitness(self, all_class: list[Subject]) -> None:
        """
        Calculates the fitness score of a schedule.
        The fitness score is a measure of how well the schedule meets the requirements.
        There will be two main criteria for the fitness evaluation and the final score will be their multiplication:
        First:
            If a class is scheduled at a time slot that is already occupied, it will not get a point.
            if at the end of a class there is no time for the next class, it will not get a point.
            if before a class there is no time for the previous class, it will not get a point.
            The max score of a class is 3 points, the minimum is 0 points.
            The score of the first part is the sum of the scores of all classes divided 
            by the count of classes * by max point (the class can get).

        Second:
            We record for each classroom and for each day the time elapsed from 7:00 a.m. to the beginning of the first
            lectures. If we have n classrooms and m working days, there will be n m of these values
            these values ​​with pi, where i takes integer values ​​from 1 to n m
            time elapsed from the end of the last lecture to 19:00 for each day and for each classroom. This one
            we mark times with ki. We form the optimality criterion in the following way:
            The sum of pi * ki for all i from 1 to n*m is the second part of the fitness score.

        The final fitness score is the product of the two parts.
        :param all_class: The list of classes.
        """

        first_score_total = 0
        max_points = 6  # max per class: 1+1+2
        total_classes = len(self.mapping)

        # First Part: Schedule Validity
        for class_index, start_slot in self.mapping.items():
            duration = all_class[class_index].get_duration()
            points = 0

            # Check before
            if start_slot == 0 or not self.class_list[start_slot - 1]:
                points += 2

            # Check after
            if start_slot + duration >= len(self.class_list) or not self.class_list[start_slot + duration]:
                points += 2

            # Check slot overlap
            overlap_penalty = 0
            for i in range(start_slot, start_slot + duration):
                if len(self.class_list[i]) > 1:
                    overlap_penalty += 1

            if overlap_penalty == 0:
                points += 2  # clean
            elif overlap_penalty == 1:
                points += 0  # mild penalty
            else:
                points -= 1  # strong penalty

            first_score_total += points

        first_part_score = first_score_total / (total_classes * max_points)

        # Second Part: Schedule Spread (Late Starts + Early Finishes)
        second_score_total = 0
        slots_per_day = 12 * 4  # 12 hours * 4 = 48 slots/day
        days = len(self.class_list) // slots_per_day

        for day_start in range(0, len(self.class_list), slots_per_day):
            slots = self.class_list[day_start: day_start + slots_per_day]

            prefix = next((i for i, s in enumerate(slots) if s), slots_per_day // 10)
            suffix = next((i for i, s in enumerate(reversed(slots)) if s), slots_per_day // 10)
            suffix = slots_per_day - suffix - 1  # Convert index from end

            if prefix == slots_per_day // 10 and suffix == slots_per_day // 10:
                # Empty day – prevent artificially high score
                prefix = suffix = slots_per_day // 10

            second_score_total += (prefix * 15) * ((slots_per_day - 1 - suffix) * 15)

        # Normalize second part (optional but improves stability)
        max_time = (15 * slots_per_day) ** 2
        second_part_score = second_score_total / (max_time * days / 4)

        # Final score: product or weighted sum
        fitness_score = first_part_score * 0.6 + 0.4 * second_part_score
        # Or try weighted sum: 0.7 * first_part_score + 0.3 * second_part_score

        self.set_fitness_score(fitness_score)
    
    def mutate(self, mutation_chance: int, all_classes: list[Subject]):
        """Function that handles the mutation of an individual.
           Based on a predefined mutation_chance, the function determines whether a mutation will happen.
           A mutation is defined as picking a random number n of classes (from 1 to a quarter of population size),
           then placing each of those n classes in a randomly picked timeslot. 
           By doing so, variability is increased and this is also a try to escape uniformness.
           """
        if random() > mutation_chance:
            self.fitness(all_classes)
            return

        num_classes = len(all_classes)

        # pick random number of classes to mutate: sometimes 1, sometimes up to 33% of classes
        n_mutate = randint(1, max(1, num_classes // 3))

        for _ in range(n_mutate):
            mutation_type = random()

            if mutation_type < 0.5:
                # relocate a random class
                class_index = randint(0, num_classes - 1)
                old_pos = self.mapping[class_index]
                duration = all_classes[class_index].duration

                # remove it from current location
                for i in range(old_pos, old_pos + duration):
                    if class_index in self.class_list[i]:
                        self.class_list[i].remove(class_index)

                # pick a *nearby* block to encourage local exploration
                current_block = old_pos // self.block_size
                block_id = current_block + randint(-1, 1)
                block_id = max(0, min(block_id, self.num_blocks - 1))

                block_start = block_id * self.block_size
                block_end = block_start + self.block_size - duration

                new_pos = randint(block_start, block_end)

                for i in range(new_pos, new_pos + duration):
                    self.class_list[i].append(class_index)
                self.mapping[class_index] = new_pos

            else:
                # swap two classes
                p = randint(0, num_classes - 1)
                q = randint(0, num_classes - 1)
                if p == q:
                    continue
                pos_p = self.mapping[p]
                pos_q = self.mapping[q]
                dur_p = all_classes[p].duration
                dur_q = all_classes[q].duration

                # check if swap would exceed schedule bounds
                if (pos_q + dur_p > len(self.class_list)) or (pos_p + dur_q > len(self.class_list)):
                    continue  # swap is impossible

                # remove both from current spots
                for i in range(pos_p, pos_p + dur_p):
                    if p in self.class_list[i]:
                        self.class_list[i].remove(p)
                for i in range(pos_q, pos_q + dur_q):
                    if q in self.class_list[i]:
                        self.class_list[i].remove(q)

                # place p at q's slot
                for i in range(pos_q, pos_q + dur_p):
                    self.class_list[i].append(p)
                self.mapping[p] = pos_q

                # place q at p's slot
                for i in range(pos_p, pos_p + dur_q):
                    self.class_list[i].append(q)
                self.mapping[q] = pos_p

        self.fitness(all_classes)

    def __repr__(self):
        return f"Schedule(class_list={self.class_list}, mapping={self.mapping}, fitness_score={self.fitness_score})"

    def __str__(self):
        return f"Schedule: {self.class_list}, {self.mapping}, {self.fitness_score}"
    
    def nice_print(self):
        """Prints out a Schedule timeslot by timeslot, to make debugging easier."""
        print("\n-------------------------------")
        print("SCHEDULE BY DAYS AND ROOMS:\n")

        slots_per_hour = 4
        hours_per_day = 12
        days_per_week = 5

        slots_per_day_per_room = hours_per_day * slots_per_hour  # 48
        slots_per_day_all_rooms = slots_per_day_per_room * (len(self.class_list) // (slots_per_day_per_room * days_per_week))
        num_rooms = len(self.class_list) // (slots_per_day_per_room * days_per_week)

        for day in range(days_per_week):
            print(f"\nDAY {day + 1}")
            for room in range(num_rooms):
                print(f"  ROOM {room + 1}")
                start = (day * slots_per_day_per_room * num_rooms) + (room * slots_per_day_per_room)
                end = start + slots_per_day_per_room
                for slot in range(start, end):
                    print(f"    Slot {slot - start:2d}: {self.class_list[slot]}")
                print("  -------------------------")
            print("*****************************")


    def write_schedule_to_html(self, classes: list[Subject], rooms, days, filename: str, population_size:int , mutation_chance:int, max_gen: int):
        """
        Write the schedule to an HTML file in a clear table format:
        - Each day has a separate table.
        - Each table shows rows for time slots and columns for rooms.
        - Each cell shows the class name(s) scheduled in that slot.
        """

        slots_per_hour = 4
        hours_per_day = 12
        slots_per_day_per_room = slots_per_hour * hours_per_day  # 48
        days_per_week = 5
        num_rooms = len(self.class_list) // (slots_per_day_per_room * days_per_week)

        html = [
            "<!DOCTYPE html>",
            "<html>",
            "<head>",
            "<meta charset='UTF-8'>",
            "<title>Raspored časova</title>",
            "<style>",
            "table { border-collapse: collapse; margin: 20px; }",
            "th, td { border: 1px solid black; padding: 5px; text-align: center; }",
            "th { background-color: #f2f2f2; }",
            "</style>",
            "</head>",
            "<body>",
            f"<h1>Raspored za SIIT (Fitness Score: {self.get_fitness_score():.2f})</h1>",
            f"<h2>Veličina populacije: {population_size}, broj generacija: {max_gen}, šansa za mutacije: {mutation_chance} </h2>"
        ]

        # For each day, create a table
        for day in range(days_per_week):
            html.append(f"<h2>{days[day]}</h2>")
            html.append("<table>")
            
            # Table header: time slot | room 1 | room 2 | ...
            header = "<tr><th>Vreme</th>"
            for room in range(num_rooms):
                header += f"<th>Učionica {rooms[room]}</th>"
            header += "</tr>"
            html.append(header)

            # For each time slot in a day
            for slot_in_day in range(slots_per_day_per_room):
                row = f"<tr><td>{7 + slot_in_day // slots_per_hour}:{(slot_in_day % slots_per_hour) * 15:02d}</td>"
                
                for room in range(num_rooms):
                    # Compute the global slot index
                    slot_idx = (day * num_rooms * slots_per_day_per_room) + (room * slots_per_day_per_room) + slot_in_day
                    slot_classes = self.class_list[slot_idx]

                    if slot_classes:
                        names = ", ".join(classes[i].name for i in slot_classes)
                    else:
                        names = "-"
                    row += f"<td>{names}</td>"

                row += "</tr>"
                html.append(row)

            html.append("</table>")

        html.append("</body>")
        html.append("</html>")

        # Write to file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(html))

        print(f"\n Schedule written to {filename}")


    def no_overlap(self):
        """Checks whether a Schedule has overlapping classes, therefore checks if it is valid.
        The logic is simple, the function checks the length of each timeslot."""

        for list in self.class_list:
            if len(list) > 1:
                # print("OVERLAP!!!!!!!! NOT GOOD!!!!")
                return False
        
        print("\n YAYYYYYY NO OVERLAP, VALID SCHEDULE!!!! \n   >>>>>>>>>>>>>>>")
        return True


def cross_over(parent1: Schedule, parent2: Schedule, class_list: list[Subject], mutations: int) -> tuple[Schedule, Schedule]:
    """
    Performs two-point crossover between two parents to produce two children.
    """
    class_count = len(parent1.mapping)
    room_count = len(parent1.class_list) // (12 * 4 * 5)
    child1 = Schedule(class_count, room_count)
    child2 = Schedule(class_count, room_count)

    # pick two random crossover points
    k1 = randint(0, class_count // 2)
    k2 = randint(class_count // 2, class_count - 1)

    # Child 1
    for i in range(k1):
        value = parent1.mapping.get(i, -1)
        child1.mapping[i] = value
        duration = class_list[i].get_duration()
        for j in range(duration):
            child1.class_list[value + j].append(i)
    for i in range(k1, k2):
        value = parent2.mapping.get(i, -1)
        child1.mapping[i] = value
        duration = class_list[i].get_duration()
        for j in range(duration):
            child1.class_list[value + j].append(i)
    for i in range(k2, class_count):
        value = parent1.mapping.get(i, -1)
        child1.mapping[i] = value
        duration = class_list[i].get_duration()
        for j in range(duration):
            child1.class_list[value + j].append(i)

    # Child 2
    for i in range(k1):
        value = parent2.mapping.get(i, -1)
        child2.mapping[i] = value
        duration = class_list[i].get_duration()
        for j in range(duration):
            child2.class_list[value + j].append(i)
    for i in range(k1, k2):
        value = parent1.mapping.get(i, -1)
        child2.mapping[i] = value
        duration = class_list[i].get_duration()
        for j in range(duration):
            child2.class_list[value + j].append(i)
    for i in range(k2, class_count):
        value = parent2.mapping.get(i, -1)
        child2.mapping[i] = value
        duration = class_list[i].get_duration()
        for j in range(duration):
            child2.class_list[value + j].append(i)

    # mutate both children
    child1.mutate(mutations, class_list)
    child2.mutate(mutations, class_list)

    return child1, child2
