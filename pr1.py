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
args = parser.parse_args()


def main():
    if args.filename is None:
        parser.print_help()
        sys.exit(1)
    data_parser = DataParser(args.filename)
    jobs, machines, tasks = data_parser.get_instance_parameters()
    instance = Instance('Roxanne', machines, jobs, tasks)
    instance.print_info()
    instance.generate_best_cmax()
    instance.johnsons_algorithm()


if __name__ == "__main__":
    main()
