import argparse
import json
from time import time

import Graph
import tcc
from SuffixArray import SuffixArray


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
    # keys = random.sample(the_dict, 1000)
    # values = [json_dict[k] for k in keys]

    keys = list(json_dict.keys())
    values = list(json_dict.values())

    U_sa = SuffixArray(keys)
    U_sa.build()

    V_sa = SuffixArray(values)
    V_sa.build()

    U = [Graph.Vertex(u) for u in keys]
    V = [Graph.Vertex(v) for v in values]

    G = Graph.BipartiteGraph(U, V)

    time_init = time()
    G.set_prefs(tcc.vertex_diff)
    # G.set_prefs(tcc.vertex_diff, (U_sa, V_sa))
    matching = G.stable_match()
    time_end = time()

    acc, errs = accuracy(matching, json_dict)

    return matching, time_end - time_init, acc, errs


def output(output_path, x, y):
    with open(output_path, 'a') as out_file:
        print(f'{x}, {y}', file=out_file)


def main():
    print('Running benchmark with arguments:', args)

    with open(args.json, 'r') as input_json:
        input_dict = json.load(input_json)

    size = len(input_dict)
    matching, sec, acc, errs = benchmark(input_dict)

    paths = args.json.split('/')
    filename = paths[-1]
    for label, value in zip(['sec', 'acc'], [sec, acc]):
        output_path = f'{args.outdir}/{filename}_{label}.csv'
        if args.reset:
            with open(output_path, 'w') as out_file:
                print('x, y', file=out_file)
        output(output_path, size, value)


if __name__ == '__main__':
    argp = argparse.ArgumentParser()
    argp.add_argument('json', type=str, help='path to .json input file')
    argp.add_argument('outdir', type=str,
                      help='directory to output time and accuracy as files')
    argp.add_argument('-r', '--reset', action='store_true',
                      help='reset file before output')
    args = argp.parse_args()

    main()
