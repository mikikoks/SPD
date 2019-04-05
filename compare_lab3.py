import os
from instance import Instance
from data_parser import DataParser
import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument("-o", "--option", type=str,
                    help="case to compare")
args = parser.parse_args()

'''
compares different methods:

-comparewithneh - compares simulated annealing with neh, returns cmaxes for datasets and checks if optimal orders are compatible
-compareinsertswap - compares neigbour generation methods, returns cmaxes for datasets and checks if optimal orders are compatible
-comparecoolingoption - compares cooling forms(temprature and iteration), returns cmaxes for datasets and checks if optimal orders are compatible
-comparecooling - compares cooling factors, returns cmaxes for datasets
-comparemove - compares classic method with method which rejects prob=1 for new better cmaxes, returns cmaxes for datasets and checks if optimal orders are compatible
-comparemovewithonlydiff - compares classic method with method which checks only different cmaxes, returns cmaxes for datasets and checks if optimal orders are compatible
-comparestart - compares start orders - neh_prio and neh_result, returns cmaxes for datasets and checks if optimal orders are compatible

classic parameters: temperature=50, min_value=0.000001, cooling=0.8, method=swap
'''


if args.option == 'comparewithneh':
    with open('compare_ex3/comparewithneh.txt', 'w') as file:
        print("INFO: Started comparing neh with simulated annealing...")
        for filename in os.listdir('data'):
            if filename.startswith('data'):
                data_parser = DataParser('data/{}'.format(filename))
                jobs, machines, tasks, neh_prio = data_parser.get_instance_parameters()
                instance = Instance('Roxanne', machines, jobs, tasks, neh_prio)
                instance.print_info()
                neh_queue, neh_cmax = instance.neh()
                simann_queues = []
                simann_cmaxes = []
                for i in range(3):
                    simann_queue, simann_cmax = instance.simulated_annealing(50, instance.neh_prio, 0.000001, 0.8, 'swap')
                    simann_cmaxes.append(simann_cmax)
                    simann_queues.append(simann_queue)
                simann_cmax_avg = sum(simann_cmaxes)/len(simann_cmaxes)
                if neh_queue in simann_queues:
                    compatibility = True
                else:
                    compatibility = False
                file.write("--- {} ---\n".format(filename))
                file.write("NEH cmax: {}\n".format(neh_cmax))
                file.write("SIMULATED ANNEALING average cmax: {}\n".format(simann_cmax_avg))
                file.write("Order compatibility: {}\n".format(compatibility))
        print("INFO: Finished!")

elif args.option == 'compareinsertswap':
    with open('compare_ex3/compareinsertswap.txt', 'w') as file:
        print("INFO: Started comparing insert with swap...")
        for filename in os.listdir('data'):
            if filename.startswith('data'):
                data_parser = DataParser('data/{}'.format(filename))
                jobs, machines, tasks, neh_prio = data_parser.get_instance_parameters()
                instance = Instance('Roxanne', machines, jobs, tasks, neh_prio)
                instance.print_info()
                simann_queues_insert = []
                simann_cmaxes_insert = []
                simann_queues_swap = []
                simann_cmaxes_swap = []
                for i in range(3):
                    simann_queue_ins, simann_cmax_ins = instance.simulated_annealing(50, instance.neh_prio, 0.000001, 0.8, 'insert')
                    simann_cmaxes_insert.append(simann_cmax_ins)
                    simann_queues_insert.append(simann_queue_ins)
                    simann_queue_swap, simann_cmax_swap = instance.simulated_annealing(50, instance.neh_prio, 0.000001, 0.8, 'swap')
                    simann_cmaxes_swap.append(simann_cmax_swap)
                    simann_queues_swap.append(simann_queue_swap)
                simann_cmax_swap_avg = sum(simann_cmaxes_swap)/len(simann_cmaxes_swap)
                simann_cmax_ins_avg = sum(simann_cmaxes_insert)/len(simann_cmaxes_insert)
                if len([queue for queue in simann_queues_swap if queue in simann_queues_insert]) != 0:
                    compatibility = True
                else:
                    compatibility = False
                file.write("--- {} ---\n".format(filename))
                file.write("SIMULATED ANNEALING insert average cmax:: {}\n".format(simann_cmax_ins_avg))
                file.write("SIMULATED ANNEALING swap average cmax: {}\n".format(simann_cmax_swap_avg))
                file.write("Order compatibility: {}\n".format(compatibility))
        print("INFO: Finished!")

elif args.option == 'comparecooling':
    with open('compare_ex3/comparecooling.txt', 'w') as file:
        print("INFO: Started comparing cooling factors...")
        for filename in os.listdir('data'):
            if filename.startswith('data'):
                data_parser = DataParser('data/{}'.format(filename))
                jobs, machines, tasks, neh_prio = data_parser.get_instance_parameters()
                instance = Instance('Roxanne', machines, jobs, tasks, neh_prio)
                instance.print_info()
                coolings = [0.8, 0.9, 0.95, 0.99]
                results = {}
                for cooling in coolings:
                    print("INFO: Cooling factor: {}".format(cooling))
                    results['cmaxes_{}'.format(cooling)] = []
                    results['queues_{}'.format(cooling)] = []
                    for i in range(3):
                        simann_queue_swap, simann_cmax_swap = instance.simulated_annealing(50, instance.neh_prio, 0.000001, cooling, 'swap')
                        results['cmaxes_{}'.format(cooling)].append(simann_cmax_swap)
                        results['queues_{}'.format(cooling)].append(simann_queue_swap)
                    results['cmax_avg_{}'.format(cooling)] = sum(results['cmaxes_{}'.format(cooling)])/len(results['cmaxes_{}'.format(cooling)])
                file.write("--- {} ---\n".format(filename))
                file.write("SIMULATED ANNEALING cooling 0.8 average cmax:: {}\n".format(results['cmax_avg_0.8']))
                file.write("SIMULATED ANNEALING cooling 0.9 average cmax: {}\n".format(results['cmax_avg_0.9']))
                file.write("SIMULATED ANNEALING cooling 0.95 average cmax: {}\n".format(results['cmax_avg_0.95']))
                file.write("SIMULATED ANNEALING cooling 0.99 average cmax: {}\n".format(results['cmax_avg_0.99']))
        print("INFO: Finished!")

elif args.option == 'comparecoolingoption':
    with open('compare_ex3/comparecoolingoption.txt', 'w') as file:
        print("INFO: Started comparing cooling options...")
        for filename in os.listdir('data'):
            if filename.startswith('data'):
                data_parser = DataParser('data/{}'.format(filename))
                jobs, machines, tasks, neh_prio = data_parser.get_instance_parameters()
                instance = Instance('Roxanne', machines, jobs, tasks, neh_prio)
                instance.print_info()
                cool_queues = []
                cool_cmaxes = []
                iter_cmaxes = []
                iter_queues = []
                for i in range(3):
                    cool_queue, cool_cmax = instance.simulated_annealing(50, instance.neh_prio, 0.000001, 0.8, 'swap')
                    cool_cmaxes.append(cool_cmax)
                    cool_queues.append(cool_queue)
                    iter_queue, iter_cmax = instance.simulated_annealing_iter(50, instance.neh_prio, 150, 'swap')
                    iter_cmaxes.append(iter_cmax)
                    iter_queues.append(iter_cmax)
                cool_cmax_avg = sum(cool_cmaxes)/len(cool_cmaxes)
                iter_cmax_avg = sum(iter_cmaxes)/len(iter_cmaxes)
                if len([queue for queue in cool_queues if queue in iter_queues]) != 0:
                    compatibility = True
                else:
                    compatibility = False
                file.write("--- {} ---\n".format(filename))
                file.write("SIMULATED ANNEALING cool option cmax: {}\n".format(cool_cmax_avg))
                file.write("SIMULATED ANNEALING iter option cmax: {}\n".format(iter_cmax_avg))
                file.write("Order compatibility: {}\n".format(compatibility))
        print("INFO: Finished!")

elif args.option == 'comparemove':
    with open('compare_ex3/comparemove.txt', 'w') as file:
        print("INFO: Started comparing move options...")
        for filename in os.listdir('data'):
            if filename.startswith('data'):
                data_parser = DataParser('data/{}'.format(filename))
                jobs, machines, tasks, neh_prio = data_parser.get_instance_parameters()
                instance = Instance('Roxanne', machines, jobs, tasks, neh_prio)
                instance.print_info()
                without_reject_queues = []
                without_reject_cmaxes = []
                with_reject_cmaxes = []
                with_reject_queues = []
                for i in range(3):
                    wo_queue, wo_cmax = instance.simulated_annealing(50, instance.neh_prio, 0.000001, 0.8, 'swap')
                    without_reject_cmaxes.append(wo_cmax)
                    without_reject_queues.append(wo_queue)
                    w_queue, w_cmax = instance.simulated_annealing_reject_prob(50, instance.neh_prio, 0.000001, 0.8, 'swap')
                    with_reject_cmaxes.append(w_cmax)
                    with_reject_queues.append(w_queue)
                w_cmax_avg = sum(with_reject_cmaxes)/len(with_reject_cmaxes)
                wo_cmax_avg = sum(without_reject_cmaxes)/len(without_reject_cmaxes)
                if len([queue for queue in without_reject_queues if queue in with_reject_queues]) != 0:
                    compatibility = True
                else:
                    compatibility = False
                file.write("--- {} ---\n".format(filename))
                file.write("SIMULATED ANNEALING with reject option cmax: {}\n".format(w_cmax_avg))
                file.write("SIMULATED ANNEALING without reject option cmax: {}\n".format(wo_cmax_avg))
                file.write("Order compatibility: {}\n".format(compatibility))
        print("INFO: Finished!")

elif args.option == 'comparestart':
    with open('compare_ex3/comparestart.txt', 'w') as file:
        print("INFO: Started comparing start options...")
        for filename in os.listdir('data'):
            if filename.startswith('data'):
                data_parser = DataParser('data/{}'.format(filename))
                jobs, machines, tasks, neh_prio = data_parser.get_instance_parameters()
                instance = Instance('Roxanne', machines, jobs, tasks, neh_prio)
                instance.print_info()
                neh_prio_queues = []
                neh_prio_cmaxes = []
                neh_result_cmaxes = []
                neh_result_queues = []
                neh_queue, neh_cmax = instance.neh()
                for i in range(3):
                    np_queue, np_cmax = instance.simulated_annealing(50, instance.neh_prio, 0.000001, 0.8, 'swap')
                    neh_prio_cmaxes.append(np_cmax)
                    neh_prio_queues.append(np_queue)
                    nr_queue, nr_cmax = instance.simulated_annealing(50, neh_queue, 0.000001, 0.8, 'swap')
                    neh_result_cmaxes.append(nr_cmax)
                    neh_result_queues.append(nr_queue)
                nr_cmax_avg = sum(neh_result_cmaxes)/len(neh_result_cmaxes)
                np_cmax_avg = sum(neh_prio_cmaxes)/len(neh_prio_cmaxes)
                if len([queue for queue in neh_prio_queues if queue in neh_result_queues]) != 0:
                    compatibility = True
                else:
                    compatibility = False
                file.write("--- {} ---\n".format(filename))
                file.write("SIMULATED ANNEALING with neh_prio start option cmax: {}\n".format(np_cmax_avg))
                file.write("SIMULATED ANNEALING with neh_result start option cmax: {}\n".format(nr_cmax_avg))
                file.write("Order compatibility: {}\n".format(compatibility))
        print("INFO: Finished!")

elif args.option == 'comparemovewithonlydiff':
    with open('compare_ex3/comparemovewithonlydiff.txt', 'w') as file:
        print("INFO: Started comparing move options (check only different cmaxes)...")
        for filename in os.listdir('data'):
            if filename.startswith('data'):
                data_parser = DataParser('data/{}'.format(filename))
                jobs, machines, tasks, neh_prio = data_parser.get_instance_parameters()
                instance = Instance('Roxanne', machines, jobs, tasks, neh_prio)
                instance.print_info()
                simann_cmaxes = []
                simann_queues = []
                onlydiff_cmaxes = []
                onlydiff_queues = []
                for i in range(3):
                    normal_queue, normal_cmax = instance.simulated_annealing(50, instance.neh_prio, 0.000001, 0.8, 'swap')
                    simann_cmaxes.append(normal_cmax)
                    simann_queues.append(normal_queue)
                    onlydiff_queue, onlydiff_cmax = instance.simulated_annealing_only_diff(50, instance.neh_prio, 0.000001, 0.8, 'swap')
                    onlydiff_cmaxes.append(onlydiff_cmax)
                    onlydiff_queues.append(onlydiff_queue)
                normal_cmax_avg = sum(simann_cmaxes)/len(simann_cmaxes)
                onlydiff_cmax_avg = sum(onlydiff_cmaxes)/len(onlydiff_cmaxes)
                if len([queue for queue in simann_queues if queue in onlydiff_queues]) != 0:
                    compatibility = True
                else:
                    compatibility = False
                file.write("--- {} ---\n".format(filename))
                file.write("SIMULATED ANNEALING normal move option cmax: {}\n".format(normal_cmax_avg))
                file.write("SIMULATED ANNEALING check only different cmaxes option cmax: {}\n".format(onlydiff_cmax_avg))
                file.write("Order compatibility: {}\n".format(compatibility))
        print("INFO: Finished!")

                

            

