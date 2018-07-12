import json
import math
import os
import sys
from glob import glob

import randomize as rdmz


def seq_gen():
    test_case_paths = glob(f'{sys.argv[1]}/*.json')
    print(f'Found {len(test_case_paths)} file(s)')

    root_out_dir = sys.argv[2] if sys.argv[2][-1] == '/' else sys.argv[2] + '/'
    for test_case_path in test_case_paths:
        print(f'\nProcessing file {test_case_path}')

        limits = range(280, 620, 40)
        num_digits = int(math.ceil(math.log10(limits[-1])))

        with open(test_case_path, 'r') as test_case_file:
            test_case_lines = [next(test_case_file) for i in range(limits[-1])]

        # splits on folder separators, gets the last
        # name and strips known '.json' suffix
        filename = test_case_path.split('/')[-1][:-5]

        out_dir = root_out_dir + filename
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        for l in limits:
            print('{:,}... '.format(l), end='')
            with open('{}/{:0{num_digits}d}.json'.format(
                    out_dir, l, num_digits=num_digits), 'w') as o:
                for i in range(l - 1):
                    print(test_case_lines[i], file=o, end='')
                print(test_case_lines[l - 1][:-2], file=o)
                print('}', file=o)
        print()


def rand_gen():
    test_case_paths = glob(f'{sys.argv[1]}/*.json')
    print(f'Found {len(test_case_paths)} file(s)')

    root_out_dir = sys.argv[2] if sys.argv[2][-1] == '/' else sys.argv[2] + '/'
    for test_case_path in test_case_paths:
        print(f'\nProcessing file {test_case_path}')

        with open(test_case_path, 'r') as test_case_file:
            test_case_dict = json.load(test_case_file)

        # all powers of 10 up to and including log10 of size of input
        # limits = [10 ** p for p in
        #           range(1, int(math.log10(len(test_case_dict)) + 1))]

        limits = range(10, 160, 10)
        num_digits = int(math.ceil(math.log10(limits[-1])))

        # splits on folder separators, gets the last
        # name and strips known '.json' suffix
        filename = test_case_path.split('/')[-1][:-5]

        out_dir = root_out_dir + filename
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        for l in limits:
            print('{:,}... '.format(l), end='')
            result = rdmz.randdict(test_case_dict, l)
            with open('{}/{:0{num_digits}d}.json'.format(
                    out_dir, l, num_digits=num_digits), 'w') as o:
                json.dump(result, o, indent=4)
        print()


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Missing arguments.'
              f' Usage:\npython {sys.argv[0]} <.json test cases directory>'
              ' <output directory>')
        exit(0)

    seq_gen()
