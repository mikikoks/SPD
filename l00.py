#!/usr/bin/env python3

import itertools

class DataParser():
    
    def __init__(self, filename):
        self.filename = filename

    def get_instance_parameters(self, filename):
        with open(filename) as f:
            print("INFO: Started parsing file {}".format(self.filename))
            first_line = f.readline()
            jobs, machines = first_line.rstrip().split(" ")
            list_of_tasks = []
            for line in f:
                n = list(int(s) for s in line.split() if s.isdigit)
                list_of_tasks.append(n)
            tasks = list_of_tasks
            return jobs, machines, tasks

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

    def generate_results(self):
        queue = self.permutation_list()
        min_makespan = self.c_max(queue)
        for option in itertools.permutations(queue):
            print(">>> For " + str(option) + " c-max value is: " + str(self.c_max(option)))
            if self.c_max(option) < min_makespan:
                queue = list(option)
                min_makespan = self.c_max(option)
        print("{} option generates minimal c-max value: {}".format(queue, min_makespan))

def main():
    parser = DataParser('data0.txt')
    jobs, machines, tasks = parser.get_instance_parameters(parser.filename)
    instance = Instance('Roxanne', machines, jobs, tasks)
    instance.print_info()
    instance.generate_results()

if __name__=="__main__":
    main()  