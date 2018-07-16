#import sys
#sys.setrecursionlimit(int(1e7))


def esc(s):
    a = []
    for c in s:
        if c == '$':
            a.append('\\')
        a.append(c)
    return "".join(a)

def idgen():
    i = 1
    while True:
        yield i
        i+=1

gen = idgen()

class N:
    def __init__(self, parent, word, p, c, wid):
        self.id = next(gen)
        self.p = p
        self.c = c
        self.word = word
        self.link = None
        self.parent = parent
        self.child = {}
        self.real = False
        self.wid = wid
        self.size = -1

    def materialize(self):
        if self.real:
            return
        self.real = True
        if self.p < len(self.word):
            self.child[self.word[self.p]] = N(self, self.word, self.p+1,self.word[self.p], self.wid)

    def get_link(self):
        if self.link:
            return self.link
        if not self.parent:
            self.link = self
            return self
        if not self.parent.parent:
            self.link = self.parent
            return self.parent
        self.link = self.parent.get_link().child[self.c]
        self.link.materialize()
        return self.link

    def add_suffix_it(self, new_word, new_word_id):
        i = 0
        x = self
        while i < len(new_word):
            x.materialize()
            ci = new_word[i]

            if ci in x.child:
                x = x.child[ci]
                i += 1
            else:
                x.child[ci] = N(x, new_word, i+1, ci, new_word_id)
                if x.parent:
                    x = x.get_link()
                else:
                    i += 1

    def search(self, term):
        i = 0
        x = self
        while i < len(term) and x.real:
            #print("searching ", term[:i+1])
            if term[i] in x.child:
                x = x.child[term[i]]
                i += 1
            else:
                break
        if not x.real:
            j = x.p
            #print("xxx", i, term[i:], x.word[x.p:])
            while i < len(term) and j < len(x.word) and term[i] == x.word[j]:
                i += 1
                j += 1
        return x.p, x.word, x.wid, x.size, i

    def calcSize(self):
        if not self.real:
            self.size = 1
        else:
            r = 0
            for k,v in self.child.items():
                v.calcSize()
                r += v.size
            self.size = r

    def dfs(self, l):
        if not self.real:
            l.append((self.p, self.word, self.wid))
        else:
            for k,v in self.child.items():
                v.dfs(l)


def CreateTree(data, suf="#$!"):
    gen = idgen()
    t = N(None, "", 0, None, 0)
    t.real = True
    import progressbar

    i = 0
    for s in progressbar.progressbar(data):
        t.add_suffix_it(s + suf + str(i), i)
        i+= 1

    t.calcSize()
    return t


