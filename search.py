#!/usr/bin/python

import numpy as np
from scipy.io import wavfile as wav
from config import *
from index import get_frames, get_fingerprint
from collections import defaultdict
from utils.koffdict import KOffDict
import sys

def read_db(dbfilename):
    result = []
    n_ranges = len(FREQ_RANGES)
    with open(dbfilename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            nums, filename = line.split('|')
            nums = map(int, nums.split(' '))
            
            fingerprint = defaultdict(lambda: set())
            for i in xrange(0, len(nums), n_ranges):
                fingerprint[tuple(nums[i:i+n_ranges])].add(i)
            result.append((KOffDict(fingerprint,
                                    n_ranges,
                                    SET_EPSILON), filename))
    return result

def find(db, input_filename):
    frames = get_frames(input_filename)
    n_ranges = len(FREQ_RANGES)

    c_max_match = (None, None)
    for i in xrange(0, SEGLEN, STEP):
        input_fingerprint = get_fingerprint(frames[i:])
        for fingerprint, filename in db:
            matches = set()
            max_score = 0
            for ridge in input_fingerprint:
                next_round = {(i, 0, 1, 0) for i in fingerprint[ridge]}
                for match in matches:
                    if match[0]+1 in fingerprint[ridge]:
                        next_round.add((match[0]+1, 0,
                                        match[2]+1, match[3]))
                    elif match[1] < SEQ_EPSILON:
                        next_round.add((match[0]+1, match[1]+1,
                                        match[2], match[3]-1))

                matches = next_round
                best = max(next_round, key = lambda x: (x[2], x[3])) if next_round else (None, None, None, None)
                c_score = (best[2], best[3])
                max_score = max(max_score, c_score)

            print max_score, filename
            c_max_match = max((max_score, filename), c_max_match)
            
    return c_max_match
        
    
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Usage:\n$ search.py [dbfilename] [input_filename]'
        sys.exit(0)
        
    dbfilename, input_filename = sys.argv[1:]

    db = read_db(dbfilename)
    print find(db, input_filename)
