import operator as op


class Vertex():
    def __init__(self, label):
        # edges list not necessary
        # because of preferences list
        self.label = label
        self.prefs = None

    def set_prefs(self, others, fn):
        """ Sets the preference list of this vertex, sorted by the results of fn.

        fn must be a function accepting two vertices and returning an integer
        that describes how closely related these two vertices are. In this
        case, the function will be called with this vertex and every other
        vertex in others. The integers will be used to sort the preference
        list. They need not be the final vertex position.
        """
        ratings = [(other, fn(self, other)) for other in others]
        ratings = sorted(ratings, key=op.itemgetter(1))
        self.prefs = [other for (other, _) in ratings]

    def __str__(self):
        return self.label

    def __repr__(self):
        return self.__str__()


class BipartiteGraph():
    def __init__(self, U, V):
        self.U = U
        self.V = V

    def stable_match(self):
        """ Irving weakly-stable marriage algorithm.

        (an extension to Gale-Shapley's).
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

    def set_prefs(self, fn):
        for u in self.U:
            u.set_prefs(self.V, fn)
        for v in self.V:
            v.set_prefs(self.U, fn)
