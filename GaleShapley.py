"""
This module performs a crappy matching, inspired by GaleShapley's stable matching.

The crappy matching only takes in account the preferences of the X partition and ignores the
preferences of the Y partition.
The main idea of this matching is that it only needs O(n * d) in memory, where d is the
maximum degree of G.
"""
class G:
    """
    A graph, to store the preferences, before running crappy matching.
    """

    def __init__(self, n):
        """
        Creates an empty graph.

        Parameters
        ----------
        n : int
            The number of vertices. Vertices will be identified by i < n.
        """
        self.p = []
        for i in range(n):
            self.p.append({})

    def grade(self, ai, bi, v):
        """
        Upgrades the weight of (ai,bi) by v in self.

        Parameters
        ----------
        ai : int
            A vertex in the X partition.
        bi : int
            A vertex in the Y partition.
        v : float
            A score, added to the current score of (ai, bi).
            If there was no score for (ai, bi), the scores is set as v.
        """
        if not bi in self.p[ai]:
            self.p[ai][bi] = 0
        self.p[ai][bi] += v

    def makeprefs(self):
        """
        Compiles the lists of preferences from self.

        Returns
        -------
        list(list(int))
            A list, containing lists of integers.
            The outer list represents the vertices in X. The inner lists represent vertices in Y.
            The vertices in the inner lists are ordered according to the preferences of X.
        """

        ps = [[(b, a) for (a,b) in x.items()] for x in self.p]
        for p in ps:
            p.sort()
            p.reverse()
        ps = [[a for (b,a) in x] for x in ps]

        return ps


def GaleShapley(ps):
    """
    Performs crappy matching.

    Parameters
    ----------
    ps : list(list(int))
        A list, containing lists of integers.
        The outer list represents the vertices in X. The inner lists represent vertices in Y.
        The vertices in the inner lists are ordered according to the preferences of X.

    Returns
    -------
    dict ( int -> int )
        Returns a dict with the matching. The keys are set from Y to X.
    """
    xs = list(range(len(ps)))
    engaged = {}
    ys = set(xs)
    while xs:
        x = xs.pop(0)
        if ps[x]:
            y = ps[x].pop(0)
            if y in engaged:
                xn = engaged[y]
                xs.append(xn)
            else:
                ys.remove(y)
            engaged[y] = x
        else:
            y = ys.pop()
            engaged[y] = x

    return engaged
