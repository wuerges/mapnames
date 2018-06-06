import json
import math
import sys
from glob import glob

import randomize as rdmz


def main():
    test_case_paths = glob(f'{sys.argv[1]}/*.json')
    print(f'Found {len(test_case_paths)} file(s)')
    for test_case_path in test_case_paths:
        print(f'\nProcessing file {test_case_path}')
        with open(test_case_path, 'r') as test_case_file:
            test_case_dict = json.load(test_case_file)
        # all powers of 10 up to and including log10 of size of input
        limits = [10 ** p for p in
                  range(1, int(math.log10(len(test_case_dict)) + 1))]
        # splits on folder separators, gets the last
        # name and strips known '.json' suffix
        filename = test_case_path.split('/')[-1][:-5]
        for l in limits:
            print('{:,}... '.format(l), end='')
            result = rdmz.randdict(test_case_dict, l)
            with open(f'{sys.argv[2]}/{filename}_{l}.json', 'w') as o:
                json.dump(result, o, indent=4)
        print()


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Missing arguments.'
              f' Usage:\npython {sys.argv[0]} <.json test cases directory>'
              ' <output directory>')
        exit(0)

    main()
