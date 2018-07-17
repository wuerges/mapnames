
class G:

    def __init__(self, n):
        self.p = []
        for i in range(n):
            self.p.append({})

    def grade(self, ai, bi, v):
        if not bi in self.p[ai]:
            self.p[ai][bi] = 0
        self.p[ai][bi] += v

    def makeprefs(self):

        print(self.p)
        ps = [[(b, a) for (a,b) in x.items()] for x in self.p]
        for p in ps:
            p.sort()
            p.reverse()
        ps = [[a for (b,a) in x] for x in ps]

        return ps


def GaleShapley(ps):
    xs = list(range(len(ps)))
    engaged = {}
    while xs:
        x = xs.pop(0)
        if ps[x]:
            y = ps[x].pop(0)
            if y in engaged:
                xn = engaged[y]
                xs.append(xn)
            engaged[y] = x

    return engaged






#g = G(10)

#g.grade(2, 3, 10)
#g.grade(2, 4, 5)

#print(g.makeprefs())
#print(GaleShapley(g.makeprefs()))

