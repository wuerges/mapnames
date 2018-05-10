import io
import sys
import Graph
import unittest as ut


class StableMatchingTest(ut.TestCase):

    # some hardcore laziness here
    def setUp(self):
        u0 = Graph.Vertex('abe')
        u1 = Graph.Vertex('bob')
        u2 = Graph.Vertex('col')
        u3 = Graph.Vertex('dan')
        u4 = Graph.Vertex('ed')
        u5 = Graph.Vertex('fred')
        u6 = Graph.Vertex('gav')
        u7 = Graph.Vertex('hal')
        u8 = Graph.Vertex('ian')
        u9 = Graph.Vertex('jon')

        Ud = {
            'abe': u0,
            'bob': u1,
            'col': u2,
            'dan': u3,
            'ed': u4,
            'fred': u5,
            'gav': u6,
            'hal': u7,
            'ian': u8,
            'jon': u9
        }

        v0 = Graph.Vertex('abi')
        v1 = Graph.Vertex('bea')
        v2 = Graph.Vertex('cath')
        v3 = Graph.Vertex('dee')
        v4 = Graph.Vertex('eve')
        v5 = Graph.Vertex('fay')
        v6 = Graph.Vertex('gay')
        v7 = Graph.Vertex('hope')
        v8 = Graph.Vertex('ivy')
        v9 = Graph.Vertex('jan')

        Vd = {
            'abi': v0,
            'bea': v1,
            'cath': v2,
            'dee': v3,
            'eve': v4,
            'fay': v5,
            'gay': v6,
            'hope': v7,
            'ivy': v8,
            'jan': v9
        }

        Ud['abe'].prefs = [Vd['abi'], Vd['eve'], Vd['cath'], Vd['ivy'],
                           Vd['jan'], Vd['dee'], Vd['fay'], Vd['bea'], Vd['hope'], Vd['gay']]
        Ud['bob'].prefs = [Vd['cath'], Vd['hope'], Vd['abi'], Vd['dee'],
                           Vd['eve'], Vd['fay'], Vd['bea'], Vd['jan'], Vd['ivy'], Vd['gay']]
        Ud['col'].prefs = [Vd['hope'], Vd['eve'], Vd['abi'], Vd['dee'],
                           Vd['bea'], Vd['fay'], Vd['ivy'], Vd['gay'], Vd['cath'], Vd['jan']]
        Ud['dan'].prefs = [Vd['ivy'], Vd['fay'], Vd['dee'], Vd['gay'],
                           Vd['hope'], Vd['eve'], Vd['jan'], Vd['bea'], Vd['cath'], Vd['abi']]
        Ud['ed'].prefs = [Vd['jan'], Vd['dee'], Vd['bea'], Vd['cath'],
                          Vd['fay'], Vd['eve'], Vd['abi'], Vd['ivy'], Vd['hope'], Vd['gay']]
        Ud['fred'].prefs = [Vd['bea'], Vd['abi'], Vd['dee'], Vd['gay'],
                            Vd['eve'], Vd['ivy'], Vd['cath'], Vd['jan'], Vd['hope'], Vd['fay']]
        Ud['gav'].prefs = [Vd['gay'], Vd['eve'], Vd['ivy'], Vd['bea'],
                           Vd['cath'], Vd['abi'], Vd['dee'], Vd['hope'], Vd['jan'], Vd['fay']]
        Ud['hal'].prefs = [Vd['abi'], Vd['eve'], Vd['hope'], Vd['fay'],
                           Vd['ivy'], Vd['cath'], Vd['jan'], Vd['bea'], Vd['gay'], Vd['dee']]
        Ud['ian'].prefs = [Vd['hope'], Vd['cath'], Vd['dee'], Vd['gay'],
                           Vd['bea'], Vd['abi'], Vd['fay'], Vd['ivy'], Vd['jan'], Vd['eve']]
        Ud['jon'].prefs = [Vd['abi'], Vd['fay'], Vd['jan'], Vd['gay'],
                           Vd['eve'], Vd['bea'], Vd['dee'], Vd['cath'], Vd['ivy'], Vd['hope']]

        Vd['abi'].prefs = [Ud['bob'], Ud['fred'], Ud['jon'], Ud['gav'],
                           Ud['ian'], Ud['abe'], Ud['dan'], Ud['ed'], Ud['col'], Ud['hal']]
        Vd['bea'].prefs = [Ud['bob'], Ud['abe'], Ud['col'], Ud['fred'],
                           Ud['gav'], Ud['dan'], Ud['ian'], Ud['ed'], Ud['jon'], Ud['hal']]
        Vd['cath'].prefs = [Ud['fred'], Ud['bob'], Ud['ed'], Ud['gav'],
                            Ud['hal'], Ud['col'], Ud['ian'], Ud['abe'], Ud['dan'], Ud['jon']]
        Vd['dee'].prefs = [Ud['fred'], Ud['jon'], Ud['col'], Ud['abe'],
                           Ud['ian'], Ud['hal'], Ud['gav'], Ud['dan'], Ud['bob'], Ud['ed']]
        Vd['eve'].prefs = [Ud['jon'], Ud['hal'], Ud['fred'], Ud['dan'],
                           Ud['abe'], Ud['gav'], Ud['col'], Ud['ed'], Ud['ian'], Ud['bob']]
        Vd['fay'].prefs = [Ud['bob'], Ud['abe'], Ud['ed'], Ud['ian'], Ud['jon'],
                           Ud['dan'], Ud['fred'], Ud['gav'], Ud['col'], Ud['hal']]
        Vd['gay'].prefs = [Ud['jon'], Ud['gav'], Ud['hal'], Ud['fred'],
                           Ud['bob'], Ud['abe'], Ud['col'], Ud['ed'], Ud['dan'], Ud['ian']]
        Vd['hope'].prefs = [Ud['gav'], Ud['jon'], Ud['bob'], Ud['abe'],
                            Ud['ian'], Ud['dan'], Ud['hal'], Ud['ed'], Ud['col'], Ud['fred']]
        Vd['ivy'].prefs = [Ud['ian'], Ud['col'], Ud['hal'], Ud['gav'],
                           Ud['fred'], Ud['bob'], Ud['abe'], Ud['ed'], Ud['jon'], Ud['dan']]
        Vd['jan'].prefs = [Ud['ed'], Ud['hal'], Ud['gav'], Ud['abe'], Ud['bob'],
                           Ud['jon'], Ud['col'], Ud['ian'], Ud['fred'], Ud['dan']]

        U = set([u0, u1, u2, u3, u4, u5, u6, u7, u8, u9])
        V = set([v0, v1, v2, v3, v4, v5, v6, v7, v8, v9])
        self.G = Graph.BipartiteGraph(U, V)

    # Test code taken from:
    # http://www.rosettacode.org/wiki/Stable_marriage_problem#Python
    def check_matching(self, matching):
        inverseengaged = dict((v, k) for k, v in matching.items())
        for he, she in matching.items():
            shelikes = she.prefs
            shelikesbetter = shelikes[:shelikes.index(he)]
            helikes = he.prefs
            helikesbetter = helikes[:helikes.index(she)]
            for guy in shelikesbetter:
                guysgirl = matching[guy]
                guylikes = guy.prefs
                if guylikes.index(guysgirl) > guylikes.index(she):
                    print(
                        f'{she.label} and {guy.label} like each other better than their present partners: {he.label} and {guysgirl.label}, respectively')
                    return False
            for gal in helikesbetter:
                girlsguy = inverseengaged[gal]
                gallikes = gal.prefs
                if gallikes.index(girlsguy) > gallikes.index(he):
                    print(
                        f'{he.label} and {gal.label} like each other better than their present partners: {she.label} and {girlsguy.label}, respectively')
                    return False
        return True

    def test_matching(self):
        capt_stdout = io.StringIO()
        sys.stdout = capt_stdout  # redirect stdout
        matching = self.G.stable_match()
        sys.stdout = sys.__stdout__  # reset redirect
        print('Captured stdout:', capt_stdout.getvalue())

        print('Resulting stable matching:')
        for (m, w) in matching.items():
            print(f'({m.label}, {w.label})')

        self.assertEqual(self.check_matching(matching), True)


if __name__ == '__main__':
    ut.main()
