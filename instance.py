import itertools
from operator import itemgetter
import json
import random
import math

class Instance():

    def __init__(self, name, machines, jobs, tasks, neh_prio):
        self.name = name
        self.machines = machines
        self.jobs = jobs
        self.tasks = tasks
        self.neh_prio = neh_prio
    
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
        makespan = 10000000
        for i in range(jobs):
            order = queue[:jobs-1]
            order.insert(i, queue[jobs-1])
            tmp_makespan = self.c_max(order)
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
        print("INFO: c-max value for optimal order: {}".format(self.neh_cmax))
        return order, makespan

    def swap(self, queue):
        num1 = 0
        num2 = 0
        while num1 == num2:
            num1 = random.randint(1,int(self.jobs))
            num2 = random.randint(1, int(self.jobs))
        index1, index2 = queue.index(num1), queue.index(num2)
        queue[index2], queue[index1] = queue[index1], queue[index2]

    def insert (self, queue):
        index = random.randint(0, int(self.jobs)-1)
        item = queue.pop(index)
        index = random.randint(0, int(self.jobs)-2)
        queue.insert(index, item)

    def simulated_annealing(self, temperature, order, min_value, cooling, method):
        if method == 'swap':
            while temperature > min_value:
                temp_order = order[:]
                self.swap(temp_order)
                temp_order_cmax = self.c_max(temp_order)
                order_cmax = self.c_max(order)
                if temp_order_cmax >= order_cmax:
                    probability_of_acceptation = math.exp((order_cmax-temp_order_cmax)/temperature)
                else:
                    probability_of_acceptation = 1
                temperature *= cooling
                p_rand = random.random()
                while p_rand == probability_of_acceptation:
                    p_rand = random.random()
                if probability_of_acceptation > p_rand:
                    order = temp_order[:]
                makespan = self.c_max(order)
        
        elif method == 'insert':
            while temperature > min_value:
                temp_order = order[:]
                self.insert(temp_order)
                temp_order_cmax = self.c_max(temp_order)
                order_cmax = self.c_max(order)
                if temp_order_cmax >= order_cmax:
                    probability_of_acceptation = math.exp((order_cmax-temp_order_cmax)/temperature)
                else:
                    probability_of_acceptation = 1
                temperature *= cooling
                p_rand = random.random()
                while p_rand == probability_of_acceptation:
                    p_rand = random.random()
                if probability_of_acceptation > p_rand:
                    order = temp_order[:]
                makespan = self.c_max(order)
        
        self.simann_queue = order
        self.simann_makespan = makespan
        print("INFO: SIMULATED ANNEALING: Optimal order for is: {}".format(self.simann_queue))
        print("INFO: SIMULATED ANNEALING: c-max value for optimal order: {}".format(self.simann_makespan))
        return order, makespan

    def simulated_annealing_iter(self, temperature, order, max_iter, method):
        if method == 'swap':
            iter = 1
            while iter < max_iter:
                temp_order = order[:]
                self.swap(temp_order)
                temp_order_cmax = self.c_max(temp_order)
                order_cmax = self.c_max(order)
                if temp_order_cmax >= order_cmax:
                    probability_of_acceptation = math.exp((order_cmax-temp_order_cmax)/temperature)
                else:
                    probability_of_acceptation = 1
                temperature = (temperature*iter)/max_iter
                iter +=1
                p_rand = random.random()
                while p_rand == probability_of_acceptation:
                    p_rand = random.random()
                if probability_of_acceptation > p_rand:
                    order = temp_order[:]
                makespan = self.c_max(order)
        
        elif method == 'insert':
            iter = 1
            while iter < max_iter:
                temp_order = order[:]
                self.insert(temp_order)
                temp_order_cmax = self.c_max(temp_order)
                order_cmax = self.c_max(order)
                if temp_order_cmax >= order_cmax:
                    probability_of_acceptation = math.exp((order_cmax-temp_order_cmax)/temperature)
                else:
                    probability_of_acceptation = 1
                temperature = (temperature*iter)/max_iter
                iter +=1
                p_rand = random.random()
                while p_rand == probability_of_acceptation:
                    p_rand = random.random()
                if probability_of_acceptation > p_rand:
                    order = temp_order[:]
                makespan = self.c_max(order)

        self.simann_queue = order
        self.simann_makespan = makespan
        print("INFO: SIMULATED ANNEALING: Optimal order is: {}".format(self.simann_queue))
        print("INFO: SIMULATED ANNEALING: c-max value for optimal order: {}".format(self.simann_makespan))
        return order, makespan

    def simulated_annealing_reject_prob(self, temperature, order, min_value, cooling, method):
        if method == 'swap':
            while temperature > min_value:
                temp_order = order[:]
                self.swap(temp_order)
                temp_order_cmax = self.c_max(temp_order)
                order_cmax = self.c_max(order)    
                probability_of_acceptation = math.exp((order_cmax-temp_order_cmax)/temperature)
                temperature *= cooling
                p_rand = random.random()
                while p_rand == probability_of_acceptation:
                    p_rand = random.random()
                if probability_of_acceptation > p_rand:
                    order = temp_order[:]
                makespan = self.c_max(order)
        
        elif method == 'insert':
            while temperature > min_value:
                temp_order = order[:]
                self.insert(temp_order)
                temp_order_cmax = self.c_max(temp_order)
                order_cmax = self.c_max(order)
                probability_of_acceptation = math.exp((order_cmax-temp_order_cmax)/temperature)
                temperature *= cooling
                p_rand = random.random()
                while p_rand == probability_of_acceptation:
                    p_rand = random.random()
                if probability_of_acceptation > p_rand:
                    order = temp_order[:]
                makespan = self.c_max(order)
        
        self.simann_queue = order
        self.simann_makespan = makespan
        print("INFO: SIMULATED ANNEALING: Optimal order for is: {}".format(self.simann_queue))
        print("INFO: SIMULATED ANNEALING: c-max value for optimal order: {}".format(self.simann_makespan))
        return order, makespan

    def simulated_annealing_only_diff(self, temperature, order, min_value, cooling, method):
        if method == 'swap':
            while temperature > min_value:
                temp_order = order[:]
                self.swap(temp_order)
                temp_order_cmax = self.c_max(temp_order)
                order_cmax = self.c_max(order)
                if temp_order_cmax > order_cmax:
                    probability_of_acceptation = math.exp((order_cmax-temp_order_cmax)/temperature)
                elif temp_order_cmax < order_cmax:
                    probability_of_acceptation = 1
                else:
                    continue
                temperature *= cooling
                p_rand = random.random()
                while p_rand == probability_of_acceptation:
                    p_rand = random.random()
                if probability_of_acceptation > p_rand:
                    order = temp_order[:]
                makespan = self.c_max(order)
                
        elif method == 'insert':
            while temperature > min_value:
                temp_order = order[:]
                self.insert(temp_order)
                temp_order_cmax = self.c_max(temp_order)
                order_cmax = self.c_max(order)
                if temp_order_cmax > order_cmax:
                    probability_of_acceptation = math.exp((order_cmax-temp_order_cmax)/temperature)
                elif temp_order_cmax < order_cmax:
                    probability_of_acceptation = 1
                else:
                    continue
                temperature *= cooling
                p_rand = random.random()
                while p_rand == probability_of_acceptation:
                    p_rand = random.random()
                if probability_of_acceptation > p_rand:
                    order = temp_order[:]
                makespan = self.c_max(order)
        
        self.simann_queue = order
        self.simann_makespan = makespan
        print("INFO: SIMULATED ANNEALING: Optimal order for is: {}".format(self.simann_queue))
        print("INFO: SIMULATED ANNEALING: c-max value for optimal order: {}".format(self.simann_makespan))
        return order, makespan
    
    @staticmethod
    def schrage_makespan(tasks):
        M=0
        cmax = 0
        for task in tasks:
            M = max(M, task[0]) + task[1]
            cmax = max(cmax, M + task[2])
        return cmax

    @staticmethod
    def handle_schrage_r(tasks):
        r = []
        for task in tasks:
            r.append(task[0])
        return r

    @staticmethod
    def handle_schrage_q(tasks):
        q = []
        for task in tasks:
            q.append(task[2])
        return q
   
    def schrage(self, unsorted_tasks): #tu dalem zmiane
        order = []
        sorted_tasks = []
        #unsorted_tasks = self.tasks[:]
        t = min(self.handle_schrage_r(unsorted_tasks))
        j = None

        while sorted_tasks or unsorted_tasks:
            while unsorted_tasks and (min(self.handle_schrage_r(unsorted_tasks)) <= t):
                tmp_list = self.handle_schrage_r(unsorted_tasks)
                j = tmp_list.index(min(tmp_list))
                sorted_tasks.append(unsorted_tasks.pop(j))
            if not sorted_tasks:
                t = min(self.handle_schrage_r(unsorted_tasks))
            else:
                q = self.handle_schrage_q(sorted_tasks)
                j = q.index(max(q))
                order.append(sorted_tasks.pop(j))
                t += order[-1][1]
        return order

    def schrage_ptmn(self, unsorted_tasks):
        sorted_tasks = []
        #unsorted_tasks = self.tasks[:]
        cmax = 0
        t = 0
        j = None
        l = [0, 0, 0]
        while sorted_tasks or unsorted_tasks:
            while unsorted_tasks and (min(self.handle_schrage_r(unsorted_tasks)) <= t):
                tmp_list = self.handle_schrage_r(unsorted_tasks)
                j = tmp_list.index(min(tmp_list))
                sorted_tasks.append(unsorted_tasks.pop(j))
                if sorted_tasks[-1][2] > l[2]:
                    l[1] = t - sorted_tasks[-1][0]
                    t = sorted_tasks[-1][0]
                    if l[1] > 0:
                        sorted_tasks.append(l)
            if not sorted_tasks:
                t = min(self.handle_schrage_r(unsorted_tasks))
            else:
                q = self.handle_schrage_q(sorted_tasks)
                j = q.index(max(q))
                task = sorted_tasks.pop(j)
                l = task[:]
                t += task[1]
                cmax = max(cmax, t + task[2])
        return cmax

    @staticmethod
    def handle_c(tasks):
        C = 0
        for task in tasks:
            C = max(C, task[0]) + task[1]
        return C

    
    def find_b(self,tasks):
        b = -1
        order_schrage = self.schrage(tasks[:])
        cmax = self.schrage_makespan(order_schrage)
        reverse_tasks = order_schrage[::-1]
        for task in reverse_tasks:
            index_of_task = order_schrage.index(task)
            if cmax == self.handle_c(order_schrage[:index_of_task+1]) + task[2]:
                b = index_of_task
                break
        return b

    def find_a(self,tasks):
        order_schrage = self.schrage(tasks[:])
        cmax = self.schrage_makespan(order_schrage)
        a = -1
        b = self.find_b(tasks)
        for index in range(b+1):
            sum = 0
            for task in order_schrage[index:b+1]:
                sum += task[1]
            if cmax == order_schrage[index][0] + sum + order_schrage[b][2]:
                a = index
                break
        return a

    def find_c(self, tasks):
        b = self.find_b(tasks)
        a = self.find_a(tasks)
        c = -1
        block = tasks[a:b+1]
        for task in block[::-1]:
            if task[2] < tasks[b][2]:
                c = tasks.index(task)
                break
        return c

    def carlier(self, ub, tasks, opt_order):
        a = -1
        b = -1
        c = -1
        lb = 0
        p_sum = 0
        order_schrage = self.schrage(tasks[:])
        u = self.schrage_makespan(order_schrage)
        if u < ub:
            ub = u
            opt_order = order_schrage[:]
        #print("UB: {}".format(ub))
        b = self.find_b(tasks)
        a = self.find_a(tasks)
        c = self.find_c(order_schrage)
        #print("b: {}, a: {}, c: {}".format(b,a,c))
        if c == -1:
            return ub
        K = order_schrage[c+1:b+1]
        r_min = min(self.handle_schrage_r(K))
        for task in K:
            p_sum += task[1]
        q_min = min(self.handle_schrage_q(K))
        hK = r_min + p_sum + q_min
        r_temp = order_schrage[c][0]
        order_schrage[c][0] = max(r_temp, r_min + p_sum) #zmieniamy r
        lb = self.schrage_ptmn(order_schrage[:])
        hKc = min(r_min, order_schrage[c][0]) + p_sum + order_schrage[c][1] + min(q_min, order_schrage[c][2])
        lb = max(hK, hKc, lb)
        #print("LB: {}".format(lb))
        if lb < ub:
            ub = min(ub, self.carlier(ub, order_schrage[:], opt_order))
        order_schrage[c][0] = r_temp #przywracamy r
        q_temp = order_schrage[c][2]
        order_schrage[c][2] = max(q_temp, p_sum + q_min)  #zmieniamy q
        lb = self.schrage_ptmn(order_schrage[:])
        hKc = min(r_min, order_schrage[c][0]) + p_sum + order_schrage[c][1] + min(q_min, order_schrage[c][2])
        lb = max(hK, hKc, lb)
        #print("LB: {}".format(lb))
        if lb < ub:
            ub = min(ub, self.carlier(ub, order_schrage[:], opt_order))
            return ub
        else:
            return ub
        order_schrage[c][2] = q_temp #przywracamy q

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