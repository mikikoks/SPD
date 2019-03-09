import argparse
import random
import re

class DataCreator():
    
    def __init__(self, filename, machines, jobs):
        self.filename = filename
        self.machines = machines
        self.jobs = jobs
    
    def run(self):
        content = str(self.jobs) + " " + str(self.machines) + "\n"
        for i in range(self.jobs):
            content += str(random.sample(range(1,10), self.machines)) + "\n"
        content = re.sub("\[|,|\]", "", content).strip()
        with open(self.filename, "w+") as file:
            file.write(content)
        file.close()

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--filename", type=str, required=True,
                     help="name of file to be created")
parser.add_argument("-m", "--machines", type=int, required=True,
                     help="number of machines")
parser.add_argument("-j", "--jobs", type=int, required=True,
                     help="number of jobs")
args = parser.parse_args()

def main():
    data_creator = DataCreator(args.filename, args.machines, args.jobs)
    data_creator.run()

if __name__ == "__main__":
    main()
