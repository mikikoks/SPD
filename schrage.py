#!/usr/bin/env python3

from data_parser import DataParser
from instance import Instance

files = ['in50.txt', 'in100.txt', 'in200.txt', 'data.001', 'data.002', 'data.003', 'data.004', 'data.005', 'data.006', 'data.007', 'data.008']
#data.003 zle, data.005 zle.
for file in files:
    data_parser = DataParser('data/schrage/{}'.format(file))
    jobs, columns, tasks = data_parser.parse_schrage()
    instance = Instance('Schrage', columns, jobs, tasks, [])
    order = instance.schrage(tasks[:]) # tu zmiana dla dodatkowego argumentu unsorted_tasks
    makespan = instance.schrage_makespan(order)
    cmax = instance.schrage_ptmn(tasks[:])
    print("INFO: Makespan for {}: {}".format(file, makespan))
    print("INFO: CMAX for {} using SchragePtmn: {}".format(file,cmax))
    opt_order = []
    u = instance.carlier(100000000,tasks[:], opt_order)
    print("INFO: >>>>>>>>>>>CMAX for {} using carlier: {}".format(file,u))