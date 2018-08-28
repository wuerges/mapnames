from optparse import OptionParser
from SuffixTree import CreateTree
from Simple import *
import json
import gc
import progressbar
import GaleShapley as gs
import Strings
from math import exp
from ortools.graph import pywrapgraph
from termcolor import colored

"""
This module is the driver program that can be used to process the testcases.
"""

parser = OptionParser(usage = "usage %prog [options] json1 json2 ...")
parser.add_option("-l", "--limit", dest="limit", type="int",
                  help="set a LIMIT ot the number of strings from input", metavar="LIMIT")

#parser.add_option("-q", "--quiet",
#                  action="store_false", dest="verbose", default=True,
#                  help="don't print status messages to stdout")

(options, args) = parser.parse_args()

if not args:
    parser.print_help()
    exit(0)
result = []
result_magic = []
result_match = []
result_ortools = []

for arg in args:
    with open(arg) as f:
        print("Working on input", arg)
        x = json.load(f)
        if type(x) is dict:
            x = [list(x.keys()), list(x.values())]

        #x = aplica(trocaPorSublinhado, x)

        if options.limit:
            x[0] = x[0][:options.limit]
            x[1] = x[1][:options.limit]
        gc.collect()

        print("Creating Tree")
        t1 = CreateTree(x[0])

        g = gs.G(len(x[0]))

        assignment = pywrapgraph.LinearSumAssignment()

        count = 0
        correct = 0
        magic = 0
        j = 0

        print("Matching Terms")
        for term in progressbar.progressbar(x[1]):
            count += 1

            # the score of the best match
            best = 0.0

            best_wid = -1
            best_term = term
            best_sz = -1

            found_magic = False

            for i in range(len(term)-1):
                p, w, wid, sz, lm = t1.search(term[i:])
                score = lm/sz
                #score = int(100000 * lm /exp(min(sz, 10)))
                #score = int(100000 * lm /(sz*sz))
                #score = int(100000 * lm/sz)
                #score = 1/sz

                if score > best:
                    best = score
                    best_term = term[i:i+lm]
                    best_sz = sz
                    best_wid = wid


 #           node, i = t1.searchNode(best_term)
 #
 #           if best_sz < 100:
 #               l = []
 #               node.dfs(l)
 #               for _, _, xwid in l:
 #                   value = int(100000 * best)
 #                   if xwid == j:
 #                       found_magic = True
 #                   g.grade(j, xwid, value)
 #                   g.grade(xwid, j, value)
 #                   assignment.AddArcWithCost(j, xwid, value)
 #           else:
 #               print(colored("\n\n\nOW SHIT", "red"), best_term)

                if sz < 10:
                #if sz < 1000:
                    node, i = t1.searchNode(term[i:])
                    #value = int(100000 * i /exp(sz))
                    value = int(100000 * i /sz)
                    l = []
                    node.dfs(l)
                    for _, _, xwid in l:
                        value2 = Strings.wagner_fischer(x[0][j], x[1][j])
                        if xwid == j:
                            found_magic = True
                        g.grade(j, xwid, value2)
                        g.grade(xwid, j, value2)
                        assignment.AddArcWithCost(j, xwid, value2)
#                else:
#                    print(colored("\n\n\nOW SHIT", "red"), best_term)

            if found_magic:
                magic += 1
            else:
                print("\n",colored("Magic Failed", "red"), x[0][j], x[1][j])
                print(colored("Best Failed","red"), x[0][best_wid], "\n")

            # greedy matching
            if j == best_wid:
                correct += 1
            j += 1

        result.append([count, correct])
        result_magic.append([count, magic])
        del t1
        gc.collect()

        ps = g.makeprefs()
        #del g

        res = gs.GaleShapley(g.p, ps)
        #print(res)

        # crappy matching
        c1 = 0
        c2 = 0
        for a, b in res.items():
            c2 += 1
            if a == b:
                c1 += 1

        # assigment
        c3 = 0
        solve_status = assignment.Solve()

        if solve_status == assignment.OPTIMAL:
            for l in range(assignment.NumNodes()):
                r = assignment.RightMate(l)
                if l == r:
                    c3 += 1

        result_match.append([c2, c1])
        result_ortools.append([c2, c3])

        print("Results without matching")
        print(result, sum(a/b for [b,a] in result)/len(result))
        print("Results using crappy matching")
        print(result_match, sum(a/b for [b,a] in result_match)/len(result_match))
        print("Results using magic")
        print(result_magic, sum(a/b for [b,a] in result_magic)/len(result_magic))
        print("Results using ortools")
        print(result_ortools, sum(a/b for [b,a] in result_ortools)/len(result_ortools))
