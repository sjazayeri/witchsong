#!/usr/bin/python

import numpy as np
from scipy.io import wavfile as wav
import numpy as np
from config import *
import sys

def product(seq):
    return reduce(lambda x, y: x*y, seq, 1)

wf = np.hamming(SEGLEN)

class Ridge(object):
    def __init__(self, freqs):
        self.freqs = tuple([x-x%(ELEMENT_EPSILON+1) for x in freqs])
        
    def __hash__(self):
        return hash(self.freqs)
        # return sum(self.freqs)-(sum(self.freqs)%(SET_EPSILON+1))
        
    def __eq__(self, r):
        n_mismatch = 0
        for f1, f2 in zip(self.freqs, r.freqs):
            if abs(f1-f2) > ELEMENT_EPSILON:
                n_mismatch += 1

        if n_mismatch > SET_EPSILON:
            return False
        return True

def keypoints(freqs, ranges):
    result = []
    for r in ranges:
        cmax, freq = None, None
        for i in xrange(r[0], r[1]):
            cval = abs(sum(freqs[i-RADIUS:i+RADIUS+1]))
            if cval > cmax:
                cmax, freq = cval, i
        result.append(freq)
    return Ridge(result)
        

def get_frames(input_filename):
    samplerate, frames = wav.read(input_filename)

    if samplerate != SAMPLERATE:
        raise NotImplemented('unsupported samplerate')

    return frames
    
    
def get_fingerprint(frames):
    if type(frames[0]) is list or type(frames[0]) is np.ndarray:
        mono = [frame[1] for frame in frames]
    else:
        mono = frames
    n_frames = len(mono)    
    
    result = []
    cnt = 0
    for i in xrange(0, n_frames-SEGLEN, SEGLEN):
        #window = mono[i:i+SEGLEN]
        #window = [window[i]*wf[i] for i in xrange(SEGLEN)]
        window = np.asarray(mono[i:i+SEGLEN])*wf
        
        dft = np.fft.fft(window)

        result.append(keypoints(dft, FREQ_RANGES))

        # cnt += 1
        # if cnt == 100:
        #    print '%s of %s done'%(i, n_frames)
        #    cnt = 0
        
    return result

    
def index(input_filename):
    frames = get_frames(input_filename)

    return get_fingerprint(frames)
        
    # mono = [frame[0] for frame in frames]
    # n_frames = len(mono)
    
    # result = []
    # cnt = 0
    # for i in xrange(0, n_frames-SEGLEN, SEGLEN):
    #     window = mono[i:i+SEGLEN]

    #     dft = np.fft.fft(window)

    #     result.append(keypoints(dft, FREQ_RANGES))

    #     cnt += 1
    #     if cnt == 100:
    #         print '%s of %s done'%(i, n_frames)
    #         cnt = 0
        
    # return result


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Usage:\n$ index.py [dbfilename] [file1] [file2] ...'
        sys.exit(0)
        
    dbfilename, input_files = sys.argv[1], sys.argv[2:]

    for f in input_files:
        with open(dbfilename, 'a') as db:
            nums = [num for ridge in index(f) for num in ridge.freqs]
            db.write(' '.join(map(str, nums)))
            db.write('|'+f+'\n')
