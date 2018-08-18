import operator as op

import numpy as np


class Vertex:
    def __init__(self, label):
        # edges list not necessary
        # because of preferences list
        self.label = label
        self.prefs = None
        self.ratings = None

    def set_prefs(self, others, h_fn):
        """ Sets the preference list of this vertex,
        sorted by the results of fn.

        :param others: set of other vertices to compute preference list against
        :param h_fn: must be a function accepting two vertices and returning
        an integer that describes how closely related these two vertices are.
        In this case, the function will be called with self and another
        vertex in others. The integers will be used to sort the preference
        list. They need not be the final vertex position.
        """
        self.ratings = [(other, h_fn(self, other)) for other in others]
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
        self.U = U if type(U) is np.ndarray else np.array(U)
        self.V = V if type(V) is np.ndarray else np.array(V)

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
        :param filters: a tuple of callables (filter on U, filter on V)
        """
        filter_on_U, filter_on_V = None, None
        if filters is not None:
            filter_on_U, filter_on_V = filters

        for these, those, filter_on_them in \
                zip([self.U, self.V],
                    [self.V, self.U],
                    [filter_on_V, filter_on_U]):
            for this in these:
                if filter_on_them is not None:
                    filtrd_idxs = filter_on_them(this.label)
                    them = those[filtrd_idxs]
                else:
                    them = those
                this.set_prefs(them, h_fn)

    def restore_prefs(self):
        for u in self.U:
            u.restore_prefs()
        for v in self.V:
            v.restore_prefs()
