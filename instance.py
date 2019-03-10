import itertools
from operator import itemgetter

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
        for option in itertools.permutations(queue):
            print(">>> For " + str(option) + " c-max value is: " + str(self.c_max(option)))
            if self.c_max(option) < min_makespan:
                queue = list(option)
                min_makespan = self.c_max(option)
        print("{} option generates minimal c-max value: {}".format(queue, min_makespan))

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
        print("Johnson's algorithm optimal order: {}".format(optimal_order))
