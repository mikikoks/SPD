import itertools

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