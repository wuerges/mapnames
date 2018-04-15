import copy as cp
import numpy as np


class Vertex():
    def __init__(self, label):
        # edges list not necessary
        # because of preferences list
        self.label = label
        self.prefs = None


class BipartiteGraph():
    def __init__(self, U, V):
        self.U = U
        self.V = V
        self.matching = None

    # Irving weakly stable marriage algorithm
    # which is an extension to Gale-Shapley's
    def stable_match(self):
        husband = {}
        self.matching = {}
        # deep copy so we don't change
        # original vertices data
        free_men = set(cp.deepcopy(self.U))
        while len(free_men) > 0:
            m = free_men.pop()
            w = m.prefs[0]

            # if some man h is engaged to w,
            # set him free
            h = husband.get(w)
            if h is not None:
                del self.matching[h]
                free_men.add(h)

            # m engages w
            self.matching[m] = w
            husband[w] = m

            # for each successor m' of m on w's preferences,
            # remove w from m's preferences so that no man
            # less desirable than m will propose w
            for i in range(w.prefs.index(m) + 1, len(w.prefs)):
                successor = w.prefs[i]
                successor.prefs.remove(w)


if __name__ == '__main__':
    u1 = Vertex('u1')
    u2 = Vertex('u2')

    v1 = Vertex('v1')
    v2 = Vertex('v2')

    u1.prefs = [v1, v2]
    u2.prefs = [v1, v2]

    v1.prefs = [u2, u1]
    v2.prefs = [u2, u1]

    U = set([u1, u2])
    V = set([v1, v2])
    G = BipartiteGraph(U, V)
    G.stable_match()

    print('Resulting stable matching:')
    for (m, w) in G.matching.items():
        print(f'({m.label}, {w.label})')
