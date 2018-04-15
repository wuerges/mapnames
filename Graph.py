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
            succ_index = w.prefs.index(m) + 1
            for i in range(succ_index, len(w.prefs)):
                successor = w.prefs[i]
                successor.prefs.remove(w)
            # and delete all m' from w so we won't attempt
            # to remove w from their list more than once
            del w.prefs[succ_index:]
