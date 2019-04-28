#!/usr/bin/env python3

from data_parser import DataParser
from instance import Instance

files = ['in50.txt', 'in100.txt', 'in200.txt']

for file in files:
    data_parser = DataParser('data/schrage/{}'.format(file))
    jobs, columns, tasks = data_parser.parse_schrage()

    instance = Instance('Schrage', columns, jobs, tasks, [])
    order = instance.schrage()
    makespan = instance.schrage_makespan(order)

    print("INFO: Makespan for {}: {}".format(file, makespan))