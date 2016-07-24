#!/usr/bin/python

from index import get_fingerprint
from scipy.io import wavfile as wav
import sys

def mismatches(frames, offset):
    f1 = get_fingerprint(frames[:-offset])
    f2 = get_fingerprint(frames[offset:])

    result = 0
    for r1, r2 in zip(f1, f2):
        if not r1 == r2:
            #print r1.freqs, r2.freqs
            result += 1

    return (result, len(f1))


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Know what? Fuck you!'
        sys.exit(0)

    offset = int(sys.argv[1])
    files = sys.argv[2:]
    for filename in files:
        sr, frames = wav.read(filename)
        if sr != 44100:
            continue
        # mono = [f[0] for f in frames]
        result = mismatches(frames, offset)
        print '%s: %d of %d mismatched'%(filename, result[0], result[1])
