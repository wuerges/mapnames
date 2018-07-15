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

    def printg1(self):
        print(r"\begin{tikzpicture}")
        print(r'\graph[tree layout, grow=down, level distance=0.5in, sibling distance=0.5in,edge quotes mid,edges={nodes={fill=white,font=\tt}},nodes={exp}] {%')
        self.printg(1)
        self.printlinks(1)
        print("};")
        print(r"\end{tikzpicture}")


    def printg(self, tab):
        if not self.child:
            print("{} [as={},imp];".format(self.id, esc(self.word[self.p:])))
        else:
            print("{} [as=];".format(self.id))
            for k,v in self.child.items():
                v.printg(tab+1);
                print("{} ->[\"{}\"] {};".format(self.id, esc(k), v.id))


    def printpgf(self, tab):
        #if not self.real:
        #    print(" " * tab, "child { node [draw,rectangle] {%s} }" % (self.word[self.p:]))
        #    #print(" " * tab, ">", self.word[self.p:])
        #else:
        if not self.child:
            #print(" " * tab, "child { node [draw, rectangle] {} }")
            print(" " * tab, "child { node [draw,rectangle] {%s} }" % esc(self.word[self.p:]))
        else:
            #print(" " * tab, "child { node [draw, circle] {%s}" % (self.word[self.p]))
            for k, v in self.child.items():
                print(" " * tab, "child { node (%d) [draw, circle] {%s}" % (v.id, esc(k)))
                v.printpgf(tab+1)
                print(" " * tab, "}")

                #print(" " * tab, k)
            #print(" " * tab, "}")

    def printlinks(self, tab):
        try:
            t = ""
            if self.id == self.get_link().id:
                t = ",loop"

            print("{} ->[dashed{}] {};".format(self.id, t, self.get_link().id))
        except:
            pass
        for k, v in self.child.items():
            v.printlinks(tab+1)



    def print(self, h):
        if h==0:
            print("digraph G {")
        if not self.real:
            print("{} [label=\"{}\"];".format(self.id, self.word[self.p:]))
        else:
            for k, v in self.child.items():
                v.print(h+1)
                print("{} -> {} [label=\"{}\"];".format(self.id, v.id, k))
        if self.link:
            print("{} -> {} [style=dotted];".format(self.link.id, self.id))
        if h==0:
            print("}")


if False:
    s = input()
    s += "$"
    gen = idgen()
    del t.child['$']
    t.print(0)


import json

t1 = N(None, "", 0, None, 0)
t1.real = True

t2 = N(None, "", 0, None, 0)
t2.real = True

with open(sys.argv[1]) as f:
    x = json.load(f)
    for i,s in enumerate(x[0]):
        t1.add_suffix_it(s, i+1)

    for i,s in enumerate(x[1]):
        t2.add_suffix_it(s, i+1)

#print(x)


