import json
import sys
from glob import glob
from time import time

import Graph
import tcc


def benchmark(json_dict):
    U = [Graph.Vertex(k) for k in json_dict.keys()]
    V = [Graph.Vertex(v) for v in json_dict.values()]

    G = Graph.BipartiteGraph(U, V)

    time_init = time()
    G.set_prefs(tcc.vertex_diff)
    matching = G.stable_match()
    time_end = time()

    return matching, time_end - time_init


def accuracy(matching, original_mapping):
    errors = []
    equal_amount = 0
    for k, v in matching.items():
        is_equal = v.label == original_mapping[k.label]
        equal_amount += int(is_equal)
        if not is_equal:
            errors.append(k)
    return equal_amount, errors


def main():
    test_case_paths = glob(f'{sys.argv[1]}/*.json')
    print(f'Found {len(test_case_paths)} test cases')
    for test_case_path in test_case_paths:
        with open(test_case_path, 'r') as test_file:
            test_json = json.load(test_file)

        matching, time_total = benchmark(test_json)
        acc, errs = accuracy(matching, test_json)

        print('path, seconds, accuracy')
        print(f'{test_case_path}, {time_total}, {acc / len(test_json)}')
        # print('Errors:')
        # for v in errs:
        #     print(f'{v.label}\n'
        #           '\twas mapped to\n'
        #           f'{matching[v].label},\n'
        #           '\tbut should have been to\n'
        #           f'{test_json[v.label]}\n')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Missing arguments.'
              f' Usage:\npython {sys.argv[0]} <.json test cases directory>')
        exit(0)

    main()
