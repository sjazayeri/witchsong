#!/usr/bin/python

import numpy as np
from scipy.io import wavfile as wav
import numpy as np
from config import *
import sys

wf = np.hamming(SEGLEN)

def damp(freqs, epsilon):
    return tuple([freq-freq%(epsilon+1) for freq in freqs])

def keypoints(freqs, ranges):
    result = []
    for r in ranges:
        cmax, freq = None, None
        for i in xrange(r[0], r[1]):
            cval = abs(freqs[i])
            if cval > cmax:
                cmax, freq = cval, i
        result.append(freq)
    return tuple(result)
        

def get_frames(input_filename):
    samplerate, frames = wav.read(input_filename)

    if samplerate != SAMPLERATE:
        raise NotImplemented('unsupported samplerate')

    return frames
    
    
def get_fingerprint(frames):
    if type(frames[0]) is np.ndarray:
        mono = [frame[1] for frame in frames]
    else:
        mono = frames
    n_frames = len(mono)    
    
    result = []
    cnt = 0
    for i in xrange(0, n_frames-SEGLEN, SEGLEN):
        window = np.asarray(mono[i:i+SEGLEN])*wf
        dft = np.fft.fft(window)
        result.append(damp(keypoints(dft, FREQ_RANGES), ELEMENT_EPSILON))

    return result

    
def index(input_filename):
    frames = get_frames(input_filename)

    return get_fingerprint(frames)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Usage:\n$ index.py [dbfilename] [file1] [file2] ...'
        sys.exit(0)
        
    dbfilename, input_files = sys.argv[1], sys.argv[2:]

    for f in input_files:
        with open(dbfilename, 'a') as db:
            nums = [num for ridge in index(f) for num in ridge]
            db.write(' '.join(map(str, nums)))
            db.write('|'+f+'\n')
