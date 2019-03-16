#!/usr/bin/env python3

import argparse
import sys
import itertools
from data_parser import DataParser
from instance import Instance
from operator import itemgetter

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--filename", type=str,
                    help="data file to be parsed")
parser.add_argument("-s", "--json", type=str,
                    default="results.json",
                    help="json file for results")
args = parser.parse_args()


def main():
    if args.filename is None:
        parser.print_help()
        sys.exit(1)
    data_parser = DataParser(args.filename)
    jobs, machines, tasks, neh_prio = data_parser.get_instance_parameters()
    instance = Instance('Roxanne', machines, jobs, tasks, neh_prio)
    instance.print_info()
    instance.generate_best_cmax()
    instance.johnsons_algorithm()
    instance.neh()
    jsonfile = "data/results/" + args.filename.split('/')[1].split('.')[0] + "_" + args.json
    instance.save_results(args.filename, jsonfile)

if __name__ == "__main__":
    main()
