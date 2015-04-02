import time


def memoize(f):
    """ Memoization decorator for functions taking one or more arguments. """

    class memodict(dict):
        def __init__(self, f):
            self.f = f

        def __call__(self, *args):
            return self[args]

        def __missing__(self, key):
            ret = self[key] = self.f(*key)
            return ret

    return memodict(f)


@memoize
def ld(s1, s2):
    """ Computes the Levenshtein distance between two input strings """
    if len(s1) == 0:

        return len(s2)

    if len(s2) == 0:

        return len(s1)
    
    return min([int(s1[0] != s2[0]) + ld(s1[1:], s2[1:]), 1 + ld(s1[1:], s2), 1 + ld(s1, s2[1:])])

@memoize
def lvd(s1, s2):
    """ Computes the Levenshtein distance between two input strings """
    if not s1: return len(s2)
    if not s2: return len(s1)
    if s1[0] == s2[0]: return lvd(s1[1:], s2[1:])
    l1 = lvd(s1, s2[1:])
    l2 = lvd(s1[1:], s2)
    l3 = lvd(s1[1:], s2[1:])
    return 1 + min(l1, l2, l3)


def levenshteinDistance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1
    distances = range(len(s1) + 1)
    for index2, char2 in enumerate(s2):
        newDistances = [index2 + 1]
        for index1, char1 in enumerate(s1):
            if char1 == char2:
                newDistances.append(distances[index1])
            else:
                newDistances.append(1 + min((distances[index1],
                                             distances[index1 + 1],
                                             newDistances[-1])))
        distances = newDistances
    return distances[-1]


start_time = time.time()
print(ld("kitten", "sitting"))
stop_time = time.time()

print stop_time - start_time

start_time = time.time()
print(lvd("kitten", "sitting"))
stop_time = time.time()

print stop_time - start_time




