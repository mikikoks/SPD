import itertools
from operator import itemgetter
import json
import random
import math

class Instance():

    def __init__(self, name, machines, jobs, tasks, neh_prio, max_iterations):
        self.name = name
        self.machines = machines
        self.jobs = jobs
        self.tasks = tasks
        self.neh_prio = neh_prio
        self.max_iterations = max_iterations
    
    def print_info(self):
        print("INFO: Instance {} consists of {} machines and {} jobs."
              .format(self.name, self.machines, self.jobs))
    
    def permutation_list(self):
        return [x+1 for x in range(0, int(self.jobs))]
    
    def generate_permutations(self):
        return list(itertools.permutations(self.permutation_list()))

    def c_max(self, queue):
        time_unit = [0] * int(self.machines)
        for item in queue:
            time_unit[0] += self.tasks[item-1][0]
            for machine_id in range(1, int(self.machines)):
                if time_unit[machine_id] < time_unit[machine_id-1]:
                    time_unit[machine_id] = time_unit[machine_id-1]
                time_unit[machine_id] += self.tasks[item-1][machine_id]
        return max(time_unit)

    def generate_best_cmax(self):
        queue = self.permutation_list()
        min_makespan = self.c_max(queue)
        makespans = []
        queues = []
        for option in itertools.permutations(queue):
            #print(">>> [C-MAX] For " + str(option) + " c-max value is: " + str(self.c_max(option)))
            if self.c_max(option) == min_makespan:
                queues.append(list(option))
                makespans.append(self.c_max(option))
            elif self.c_max(option) < min_makespan:
                queue = list(option)
                min_makespan = self.c_max(option)

        indexes = [i for i, x in enumerate(makespans) if x == min_makespan]

        print("INFO: C-MAX: {} option generates minimal c-max value: {}".format(queue, min_makespan))
        self.cmax_queue = [queue]
        self.cmax_makespan = [min_makespan]
        if indexes:
            for i in indexes:
                self.cmax_queue.append(queues[i])
                self.cmax_makespan.append(makespans[i])
                print("INFO: C-MAX: {} option generates minimal c-max value: {}".format(queues[i], makespans[i]))

    def johnsons_algorithm(self):
        virtual_tasks = [[] for  i in range(len(self.tasks))]
        optimal_begining = []
        optimal_ending = []
        list_of_jobs = self.permutation_list()
        if self.machines == "3":
            for item in range(len(self.tasks)):
                virtual_tasks[item] = [self.tasks[item][0] + self.tasks[item][1], self.tasks[item][1] + self.tasks[item][2]]
        elif self.machines == "2":
            virtual_tasks = self.tasks.copy()
        while len(virtual_tasks) != 0:
            p1 = min(virtual_tasks, key=itemgetter(0))
            p2 = min(virtual_tasks, key=itemgetter(1))
            if p1[0] <= p2[1]:
                index_of_p1 = virtual_tasks.index(p1)
                optimal_begining.append(list_of_jobs.pop(index_of_p1))
                virtual_tasks.remove(p1)
            else:
                index_of_p2 = virtual_tasks.index(p2)
                optimal_ending.insert(0, list_of_jobs.pop(index_of_p2))
                virtual_tasks.remove(p2)

        self.johnson_queue = optimal_begining + optimal_ending
        self.johnson_cmax = self.c_max(self.johnson_queue)
        print("INFO: JOHNSON: Optimal order for Johnson's algorithm is: {}".format(self.johnson_queue))
        print("INFO: JOHNSON: {} generates c-max value: {}".format(self.johnson_queue, self.johnson_cmax))

    def neh_insertion(self, queue):
        jobs = len(queue)
        optimal_order = queue
        makespan = self.c_max(optimal_order)
        for i in range(jobs):
            order = queue[:jobs-1]
            order.insert(i, queue[jobs-1])
            tmp_makespan = self.c_max(order)
            #print(">>> [NEH] For " + str(order) + " c-max value is: " + str(self.c_max(order)))
            if tmp_makespan < makespan:
                makespan = tmp_makespan
                optimal_order = order
        return optimal_order, makespan


    def neh(self):
        for i in range(2, int(self.jobs)+1):
            order, makespan = self.neh_insertion(self.neh_prio[:i])
            self.neh_prio[:i] = order
        self.neh_queue = order
        self.neh_cmax = makespan
        print("INFO: NEH: Optimal order for Neh's algorithm is: {}".format(self.neh_queue))
        print("INFO: NEH: {} generates c-max value: {}".format(self.neh_queue, self.neh_cmax))


    def swap(self, queue):
        num1 = 0
        num2 = 0
        while num1 == num2:
            num1 = random.randint(1,int(self.jobs))
            num2 = random.randint(1, int(self.jobs))
        index1, index2 = queue.index(num1), queue.index(num2)
        queue[index2], queue[index1] = queue[index1], queue[index2]


    def simulated_annealing(self, temperature, order, iteration):
        if iteration < self.max_iterations:
            temp_order = order[:]
            self.swap(temp_order)
            temp_order_cmax = self.c_max(temp_order)
            order_cmax = self.c_max(order)
            if temp_order_cmax >= order_cmax:
                probability_of_acceptation = math.exp((order_cmax-temp_order_cmax)/temperature)
            else:
                probability_of_acceptation = 1
            #temperature = ( temperature * iteration ) / self.max_iterations
            temperature *= 0.8
            iteration += 1
            if probability_of_acceptation >= random.random():
                return self.simulated_annealing(temperature, temp_order, iteration)
            else:
                return self.simulated_annealing(temperature, order, iteration)
        else:
            return order





    def save_results(self, filename, algorithm, json_to_write):
        data = {}
        data['filename'] = filename
        if algorithm == 'bruteforce':
            data['cmax_queues'] = self.cmax_queue
            data['cmax_makespans'] = self.cmax_makespan
        elif algorithm == 'johnson':
            data['johnson_queue'] = self.johnson_queue
            data['johnson_cmax'] = self.johnson_cmax
        elif algorithm == 'neh':
            data['neh_queue'] = self.neh_queue
            data['neh_cmax'] = self.neh_cmax
        json_data = json.dumps(data)
        with open (json_to_write, 'w+') as file:
            file.write(json_data)
            

