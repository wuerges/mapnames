import sys
import tcc
import json
import Graph
import pprint
from time import time


def main():
    if len(sys.argv) < 2:
        print(
            f'Missing arguments. Usage:\npython {sys.argv[0]} <json file>')
        exit(0)

    init_time = time()

    with open(sys.argv[1], 'r') as f:
        map = json.load(f)

    pp = pprint.PrettyPrinter(indent=4)
    U = [Graph.Vertex(k) for k in map.keys()]
    V = [Graph.Vertex(v) for v in map.values()]

    G = Graph.BipartiteGraph(U, V)
    prefs_time_init = time()
    G.set_prefs(tcc.vertex_diff)
    prefs_time_end = time()

    # print('Final U preferences:')
    # for u in G.U:
    #     print(u, '=')
    #     pp.pprint(u.prefs)
    #
    # print('\nFinal V preferences:')
    # for v in G.V:
    #     print(v, '=')
    #     pp.pprint(v.prefs)

    matching_time_init = time()
    matching = G.stable_match()
    matching_time_end = time()

    print('\nFinal matching:')
    pp.pprint(matching)

    print(
        f'Setting preferences took {prefs_time_end - prefs_time_init} seconds')
    print(f'Matching took {matching_time_end - matching_time_init} seconds')
    print(f'Total time spent was {matching_time_end - init_time} seconds')


if __name__ == '__main__':
    main()
