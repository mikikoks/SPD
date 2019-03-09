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
            return jobs, machines, tasks