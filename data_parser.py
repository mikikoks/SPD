import os
import sys

class DataParser():
    
    def __init__(self, filename):
        self.filename = filename

    def get_instance_parameters(self):
        if not os.path.isfile(self.filename):
            print("ERROR: File not found")
            sys.exit(1)
        with open(self.filename) as f:
            print("INFO: Started parsing file {}".format(self.filename))
            first_line = f.readline()
            jobs, machines = first_line.rstrip().split(" ")
            list_of_tasks = []
            for line in f:
                n = list(int(s) for s in line.split() if s.isdigit)
                list_of_tasks.append(n)
        tasks = list_of_tasks
        order = []
        dict = {}
        for i in range(int(jobs)):
            dict[str(i)] = tasks[i]
        for key,value in sorted(dict.items(),key=lambda i:sum(i[1]),reverse=True):
            order.append(int(key)+1)
        return jobs, machines, tasks, order

    def parse_schrage(self):
        if not os.path.isfile(self.filename):
            print("ERROR: File not found")
            sys.exit(1)
        with open(self.filename) as f:
            print("INFO: Started parsing file {}".format(self.filename))
            first_line = f.readline()
            jobs, columns = (int(s) for s in first_line.split() if s.isdigit())
            list_of_tasks = []
            for line in f:
                n = list(int(s) for s in line.split() if s.isdigit())
                list_of_tasks.append(n)
        tasks = list_of_tasks
        return jobs, columns, tasks
