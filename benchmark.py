import sys
import tcc
import json
import Graph
import functools as ft
from glob import glob
from time import time


def benchmark(json_dict):
    U = [Graph.Vertex(k) for k in json_dict.keys()]
    V = [Graph.Vertex(v) for v in json_dict.values()]

    G = Graph.BipartiteGraph(U, V)

    time_init = time()
    G.set_prefs(tcc.vertex_diff)
    matching = G.stable_match()
    time_end = time()

    return matching, time_end - time_init


def accuracy(mapping):
    positives_amount = ft.reduce(
        lambda amount, item: amount + int(item[0] == item[1]), mapping.items(),
        0)
    return positives_amount / len(mapping)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Missing arguments.'
              f' Usage:\npython {sys.argv[0]} <.json test cases directory>')
        exit(0)

    test_case_paths = glob(f'{sys.argv[1]}/*.json')
    print(f'Found {len(test_case_paths)} test cases')
    for test_case_path in test_case_paths:
        with open(test_case_path, 'r') as test_file:
            test_json = json.load(test_file)

        matching, time_total = benchmark(test_json)
        acc = accuracy(matching)

        print(f'{test_case_path}: {time_total} seconds and {acc} accuracy')
