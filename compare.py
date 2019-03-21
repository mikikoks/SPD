from instance import Instance
from data_parser import DataParser
from data_creator import DataCreator
import time
import json

data_creator = DataCreator('compare/compare0.txt', 2, 2)
data_parser = DataParser('compare/compare0.txt')

def main():
    for i in range(3,11):
        result = 'compare/results/result_2ma_' + str(i)
        data_creator.filename = 'compare/data/compare_2ma_' + str(i) + '.txt'
        data_creator.jobs = i
        data_creator.run()
        data_parser.filename = data_creator.filename
        jobs, machines, tasks, neh_prio = data_parser.get_instance_parameters()
        instance = Instance(str(i), machines, jobs, tasks, neh_prio)
        instance.print_info()
        start = time.time()
        instance.generate_best_cmax()
        end = time.time()
        bruteforce_time = end - start
        instance.save_results(data_parser.filename, 'bruteforce', result + '_bruteforce.json')
        start = time.time()
        instance.johnsons_algorithm()
        end = time.time()
        johnson_time = end - start
        instance.save_results(data_parser.filename, 'johnson', result + '_johnson.json')
        start = time.time()
        instance.neh()
        end = time.time()
        neh_time = end - start
        instance.save_results(data_parser.filename, 'neh', result + '_neh.json')
        print("INFO:\tBruteforce: " + str(bruteforce_time) + "\n\tJohnson: " + str(johnson_time) + "\n\tNeh: " + str(neh_time))
        times = {}
        times['filename'] = data_parser.filename
        times['bruteforce_time'] = str(bruteforce_time)
        times['johnson_time'] = str(johnson_time)
        times['neh_time'] = str(neh_time)
        times_json = json.dumps(times)
        filename = 'compare/results/result_2ma_' + str(i) + '_times.json'
        with open (filename, 'w+') as f:
            f.write(times_json)

if __name__ == '__main__':
    main()