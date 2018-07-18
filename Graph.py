import operator as op

import numpy as np


class Vertex:
    def __init__(self, label):
        # edges list not necessary
        # because of preferences list
        self.label = label
        self.prefs = None
        self.ratings = None

    def set_prefs(self, others, fn, filter_fn=None):
        """ Sets the preference list of this vertex,
        sorted by the results of fn.

        :param others: set of other vertices to compute preference list against
        :param fn: must be a function accepting two vertices and returning
        an integer that describes how closely related these two vertices are.
        In this case, the function will be called with self and another
        vertex in others. The integers will be used to sort the preference
        list. They need not be the final vertex position.
        :param filter_fn: a function taking self.label to filter vertices
        in others to compare self to. Must return a list of indices over others.
        """
        if filter_fn is None:
            self.ratings = [(other, fn(self, other)) for other in others]
        else:
            self.ratings = [[others[i], np.inf] for i in range(len(others))]
            indices_fn = filter_fn(self.label)
            print(self.label, len(indices_fn))
            for i in indices_fn:
                self.ratings[i][1] = fn(self, others[i])
            self.ratings.sort(key=op.itemgetter(1))
            self.restore_prefs()

    def restore_prefs(self):
        self.prefs = [other for (other, _) in self.ratings]

    def __str__(self):
        return self.label

    def __repr__(self):
        return self.__str__()


class BipartiteGraph:
    def __init__(self, U, V):
        self.U = U
        self.V = V

    def stable_match(self):
        """ Irving weakly-stable marriage algorithm.

        (an extension to Gale-Shapley's).
        :return: a dict mapping the vertices of U to V.
        """
        husband = {}
        matching = {}
        # preferences list will get screwed...
        free_men = set(self.U)
        while len(free_men) > 0:
            m = free_men.pop()
            w = m.prefs[0]

            # if some man h is engaged to w,
            # set him free
            h = husband.get(w)
            if h is not None:
                del matching[h]
                free_men.add(h)

            # m engages w
            matching[m] = w
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
        return matching

    def set_prefs(self, h_fn, filters=None):
        """ Sets the preference list for all u in self.U and all v in self.V.

        :param h_fn: see Vertex.set_prefs()
        :param filters: a tuple of callables (filter for U, filter for V)
        """
        filter_U, filter_V = None, None
        if filters is not None:
            filter_U, filter_V = filters

        print('U')
        for u in self.U:
            u.set_prefs(self.V, h_fn, filter_V)
        print('V')
        for v in self.V:
            v.set_prefs(self.U, h_fn, filter_U)

    def restore_prefs(self):
        for u in self.U:
            u.restore_prefs()
        for v in self.V:
            v.restore_prefs()
