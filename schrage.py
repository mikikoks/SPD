#!/usr/bin/env python3

from data_parser import DataParser
from instance import Instance

files = ['in50.txt', 'in100.txt', 'in200.txt', 'data.001']

for file in files:
    data_parser = DataParser('data/schrage/{}'.format(file))
    jobs, columns, tasks = data_parser.parse_schrage()
    instance = Instance('Schrage', columns, jobs, tasks, [])
    order, pi = instance.schrage(instance.tasks)
    makespan = instance.schrage_makespan(order)
    cmax = instance.schrage_ptmn(instance.tasks)
    print("INFO: Carlier for {} started...".format(file))
    carlier = instance.carlier(pi, instance.tasks)
    #print("INFO: CMAX for {} using Schrage: {}".format(file, makespan))
    #print("INFO: CMAX for {} using SchragePtmn: {}".format(file,cmax))
    #print("INFO: CMAX for {} using Carlier: {}".format(file,carlier))
    