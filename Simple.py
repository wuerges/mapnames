import re

def trocaPorSublinhado(t):
    return re.sub(r'[\[\]\(\)]', '_', t)


def aplica(f, t):
    a, b = t
    return [list(map(f, a)), list(map(f, b))]
