from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model
from pathlib import Path

class RPQ():
    def __init__(self,r,p,q):
        self.R = r
        self.P = p
        self.Q = q

def MILP(jobs, instanceName):
    variablesMaxValue = 0
    for i in range(len(jobs)):
        variablesMaxValue += (jobs[i].R + jobs[i].P + jobs[i].Q)

    solver = pywraplp.Solver('simple_mip_program',pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    alfasMatrix = {}
    for i in range(len(jobs)):
        for j in range(len(jobs)):
            alfasMatrix[i,j] = solver.IntVar(0,1,"alfa"+str(i)+"_"+str(j))
    starts = []

    for i in range(len(jobs)):
        starts.append(solver.IntVar(0,variablesMaxValue,"starts"+str(i)))
    cmax = solver.IntVar(0,variablesMaxValue,"cmax")

    for i in range(len(jobs)):
        solver.Add(starts[i]>=jobs[i].R)
        solver.Add(cmax>=starts[i]+jobs[i].P+jobs[i].Q)

    for i in range(len(jobs)):
        for j in range(i+1,len(jobs)):
            solver.Add(starts[i]+jobs[i].P <= starts[j] + alfasMatrix[i,j]*variablesMaxValue)
            solver.Add(starts[j]+jobs[j].P <= starts[i] + alfasMatrix[j,i]*variablesMaxValue)
            solver.Add(alfasMatrix[i,j]+alfasMatrix[j,i]==1)

    solver.Minimize(cmax)
    status = solver.Solve()
    if (status is not pywraplp.Solver.OPTIMAL):
        print("Not optimal!")
    print(instanceName, "MILP Cmax: ", solver.Objective().Value())
    pi = []
    for i in range(len(starts)):
        pi.append((i,starts[i].solution_value()))
    pi.sort(key=lambda x: x[1])
    print(pi)

def CP(jobs, instanceName):

    variablesMaxValue = 0
    for i in range(len(jobs)):
        variablesMaxValue += (jobs[i].R + jobs[i].P + jobs[i].Q)

    model = cp_model.CpModel()
    solver = cp_model.CpSolver()

    alfasMatrix = {}
    for i in range(len(jobs)):
        for j in range(len(jobs)):
            alfasMatrix[i,j] = model.NewIntVar(0,1,"alfa"+str(i)+"_"+str(j))

    starts = []
    for i in range(len(jobs)):
        starts.append(model.NewIntVar(0,variablesMaxValue,"starts"+str(i)))

    cmax = model.NewIntVar(0,variablesMaxValue,"cmax")

    for i in range(len(jobs)):
        model.Add(starts[i]>=jobs[i].R)
        model.Add(cmax>=starts[i]+jobs[i].P+jobs[i].Q)

    for i in range(len(jobs)):
        for j in range(i+1,len(jobs)):
            model.Add(starts[i]+jobs[i].P <= starts[j] + alfasMatrix[i,j]*variablesMaxValue)
            model.Add(starts[j]+jobs[j].P <= starts[i] + alfasMatrix[j,i]*variablesMaxValue)
            model.Add(alfasMatrix[i,j]+alfasMatrix[j,i]==1)

    model.Minimize(cmax)
    status = solver.Solve(model)
    if (status is not cp_model.OPTIMAL):
        print("Not optimal!")
    print(instanceName, "CP Cmax: ", solver.ObjectiveValue())
    pi = []
    for i in range(len(starts)):
        pi.append((i,solver.Value(starts[i])))
    pi.sort(key=lambda x: x[1])
    print(pi)

def GetRPQsFromFile(pathToFile):
    fullTextFromFile = Path(pathToFile).read_text()
    words = fullTextFromFile.replace("\n"," ").split(" ")
    words_cleaned = list(filter(None,words))
    numbers = list(map(int, words_cleaned))

    numbersOfJobs = numbers[0]
    numbers.pop(0)
    numbers.pop(0)

    jobs = []
    for i in range(numbersOfJobs):
        jobs.append(RPQ(numbers[0],numbers[1],numbers[2]))
        numbers.pop(0)
        numbers.pop(0)
        numbers.pop(0)

    return jobs

if __name__ == '__main__':
    file_paths = ["data/schrage/data.000",
                  "data/schrage/data.000b", 
                  "data/schrage/data.000c", 
                  "data/schrage/data.000d"]
    file_paths_cp = ["data/schrage/in50.txt",
                     "data/schrage/in100.txt"]

    for i in range(len(file_paths)):
        jobs = GetRPQsFromFile(file_paths[i])
        MILP(jobs,file_paths[i])
        CP(jobs,file_paths[i])
    
    for i in range(len(file_paths_cp)):
        jobs = GetRPQsFromFile(file_paths_cp[i])
        CP(jobs,file_paths_cp[i])
    