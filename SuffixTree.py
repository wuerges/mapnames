import sys
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
    for i,s in enumerate(data):
        t.add_suffix_it(s + suf + str(i), i)
    t.calcSize()
    return t

import json

with open(sys.argv[1]) as f:
    ds = json.load(f)

    x = [[],[]]
    for k,v in ds.items():
        x[0].append(k)
        x[1].append(v)

    if len(sys.argv) > 2:
        cut = int(sys.argv[2])
        x[0] = x[0][:cut]
        x[1] = x[1][:cut]

    t1 = CreateTree(x[0])
    #t2 = CreateTree(x[1])

    count = 0
    correct = 0
    for j, term in enumerate(x[1]):
        count += 1
        #best = 1000
        best = 0
        best_wid = -1
        best_term = term
        best_sz = -1
        for i in range(len(term)-1):
            p, w, wid, sz, lm = t1.search(term[i:])
            if lm > best:
            #if sz < best:
                best = lm
                best_term = term[i:i+lm]
                best_sz = sz
                best_wid = wid

        if j == best_wid:
            correct += 1
        else:
            print("-"*10)
            print(j, best_wid, best_sz, best_term)
            print("original:", term)
            print("cut:", best_term)
            print(x[0][j])
            print(x[1][j])
            print(x[0][best_wid])
            print(x[1][best_wid])

    print(count, correct)



