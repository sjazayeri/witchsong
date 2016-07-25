#!/usr/bin/python

from itertools import combinations

class KOffDict(object):
    '''A static dict-like datastructure whose keys are n-element
    tuples and whose values are sets, accessing a key q will return
    the union of all values whose keys differ from q in at most k
    locations'''
    
    def __init__(self, d, seq_len, k):
        ''':param d the dictionary from which the datastructure
        is to be built
        :param seq_len the length of the keys
        :param k maximum mismatch'''
    
        self.seq_len = seq_len
        self.k = k
        self.d = dict()

        for key, value in d.iteritems():
            self.d[key] = set(value)
            for locs in combinations(xrange(self.seq_len), self.k):
                c_key = list(key)
                for loc in locs:
                    c_key[loc] = None
                c_key = tuple(c_key)
                c_val = self.d.get(c_key, None)
                if c_val:
                    c_val.update(value)
                else:
                    self.d[c_key] = set(value)

                    
    def __getitem__(self, key):
        result = self.d.get(key, set())
        for locs in combinations(xrange(self.seq_len), self.k):
            c_key = list(key)
            for loc in locs:
                c_key[loc] = None
            c_key = tuple(c_key)
            result.update(self.d.get(c_key, set()))
        return result
