import itertools
from operator import itemgetter
import json

class Instance():

    def __init__(self, name, machines, jobs, tasks):
        self.name = name
        self.machines = machines
        self.jobs = jobs
        self.tasks = tasks
    
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
            print(">>> [C-MAX] For " + str(option) + " c-max value is: " + str(self.c_max(option)))
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

        optimal_order = optimal_begining + optimal_ending
        makespan = self.c_max(optimal_order)
        print("INFO: JOHNSON: Optimal order for Johnson's algorithm is: {}".format(optimal_order))
        print("INFO: JOHNSON: {} generates c-max value: {}".format(optimal_order, makespan))
        self.johnson_queue = optimal_order
        self.johnson_cmax = makespan

    def save_results(self, filename, json_to_write):
        data = {}
        data['filename'] = filename
        data['cmax_queues'] = self.cmax_queue
        data['cmax_makespans'] = self.cmax_makespan
        data['johnson_queue'] = self.johnson_queue
        data['johnson_cmax'] = self.johnson_cmax
        json_data = json.dumps(data)
        with open (json_to_write, 'w+') as file:
            file.write(json_data)
            

