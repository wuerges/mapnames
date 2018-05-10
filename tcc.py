import numpy as np


def wagner_fischer(str1, str2):
    D = np.empty((len(str1) + 1, len(str2) + 1), dtype=np.int64)
    # Positions of D represent the lengths of str1 and str2, respectively, so:
    # D[0][0] = 0 because there is no operation to do on empty strings
    # D[i][0] = D[i - 1][0] + 1 (cost of deletion) for i from
    # 1 to len(str1) 'cause the only thing to do is delete all
    # characters of str1 until ''. Same for D[0][j].
    D[:, 0] = np.arange(len(str1) + 1)
    D[0, :] = np.arange(len(str2) + 1)
    for i in np.arange(1, len(str1) + 1):
        for j in np.arange(1, len(str2) + 1):
            # Change operation
            cost1 = D[i - 1][j - 1] + int(str1[i - 1] != str2[j - 1])
            # Minimum of deletion and insertion operations
            # Deletion means cost of transforming str1[0..i-1]
            # to str2[0..j] and deleting str1[i]
            # Insertion means cost of transforming str[0..i]
            # to str2[0..j-1] and inserting str2[j]
            cost2 = np.minimum(D[i - 1][j] + 1, D[i][j - 1] + 1)
            D[i][j] = np.minimum(cost1, cost2)
    # [-1][-1] is the last column of the last row, which holds the edit
    # distance of the whole str1 and str2 strings
    return D[-1][-1]


# Did not put on Vertex class because
# this is too non-standard for graphs
def vertex_diff(u, v):
    return wagner_fischer(u.label, v.label)
