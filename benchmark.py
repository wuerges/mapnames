import json
import os
import sys
from time import time

import Graph
import tcc


def accuracy(matching, original_mapping):
    errors = []
    equal_amount = 0
    for k, v in matching.items():
        is_equal = v.label == original_mapping[k.label]
        equal_amount += int(is_equal)
        if not is_equal:
            errors.append(k)
    return equal_amount / len(matching), errors


def benchmark(json_dict):
    U = [Graph.Vertex(k) for k in json_dict.keys()]
    V = [Graph.Vertex(v) for v in json_dict.values()]

    G = Graph.BipartiteGraph(U, V)

    time_init = time()
    G.set_prefs(tcc.vertex_diff)
    matching = G.stable_match()
    time_end = time()

    acc, errs = accuracy(matching, json_dict)

    return matching, time_end - time_init, acc, errs


def output(out_file_path, x, y):
    if os.path.exists(out_file_path):
        with open(out_file_path, 'a') as outf:
            print(f'{x}, {y}', file=outf)
    else:
        with open(out_file_path, 'w') as outf:
            print('x, y', file=outf)
            print(f'{x}, {y}', file=outf)


def run_for_file(test_case_path):
    with open(test_case_path, 'r') as test_file:
        test_json = json.load(test_file)

    matching, sec, acc, errs = benchmark(test_json)

    paths = test_case_path.split('/')
    out_dir = paths[0]
    test_case = paths[1]
    size = paths[-1][:-5]

    out_sec_path = f'{out_dir}/{test_case}_sec.csv'
    out_acc_path = f'{out_dir}/{test_case}_acc.csv'

    # print(out_sec_path, size, sec)
    # print(out_acc_path, size, acc)

    output(out_sec_path, size, sec)
    output(out_acc_path, size, acc)

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
              f' Usage:\npython {sys.argv[0]} <.json file>')
        exit(0)

    run_for_file(sys.argv[1])
