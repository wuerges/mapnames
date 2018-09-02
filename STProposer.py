
from SuffixTree import CreateTree
import progressbar

x = [list(x.keys()), list(x.values())]


class STProposer:
    def __init__(self, left, right, graphs):
        self.left = left
        self.right = right
        self.graphs = graphs
        self.tree = None


    def initialize(self):
        self.tree = CreateTree(self.left)

    def initialize_mappings(self):
        print("Matching Terms")
        for j, term in enumerate(progressbar.progressbar(self.left)):
            for i in range(len(term)-1):
                p, w, wid, sz, lm = self.tree.search(term[i:])

                l = []
                node.dfs(l)

                for g in self.graphs:
                    g.add_arc(j, wid, p, sz, lm, term)

