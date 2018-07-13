import operator as op


class SuffixArray:
    def __init__(self, strings):
        """ Saves the strings for later building.

        Does not build the Suffix Array. Call self.build() for that.

        :param strings: list of strings to build the Suffix Array on
        """
        self.strings = strings
        self.suffixes = None

    def build(self):
        """ Builds the Suffix Array based on saved strings """
        self.suffixes = [(self.strings[i][j:], i, j)
                         for i in range(len(self.strings))
                         for j in range(len(self.strings[i]))]
        self.suffixes.sort()

    def binary_search(self, string, lower=True):
        """ Searches for lower or upper bound for string
        on self.suffixes with a binary search.

        Method based on stringMatching function from
        Competitive Programming 3 book (page 259).

        :param string: string to search for
        :param lower: True to return the lower bound or
                      False to return the upper bound
        :return: the lower or upper bound, according to lower
        """
        if lower:
            cmp = op.ge
        else:
            cmp = op.gt
        lo, hi = 0, len(self.suffixes) - 1
        while lo < hi:
            mid = int(lo + (hi - lo) / 2)
            suffix = self.suffixes[mid][0]
            # print(lo, mid, hi, suffix)
            if cmp(suffix[:len(string)], string):
                hi = mid
            else:
                lo = mid + 1
        # special case: if searching for upper bound and
        # last suffix is not equal to the query string,
        # then decrease upper bound (should we?)
        if not lower:
            if self.suffixes[hi][0][:len(string)] != string:
                hi -= 1
        return lo if lower else hi

    def search_bounds(self, string):
        """ Searches for both lower and upper bounds
        for string on self.suffixes.

        :param string: string to search for
        :return: tuple containing lower and upper bounds
        """
        lower_bound = self.binary_search(string)
        higher_bound = self.binary_search(string, lower=False)
        return lower_bound, higher_bound


query = 'GATACA'
sa = SuffixArray(['GATAGACA'])
sa.build()
print(sa.suffixes)
lo, hi = sa.search_bounds(query)
print(lo, sa.suffixes[lo], hi, sa.suffixes[hi])
