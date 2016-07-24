#!/usr/bin/python

import numpy as np
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt
from scipy.io import wavfile as wav
import sys

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y


if __name__ == '__main__':
    input_filename, output_filename = sys.argv[1], sys.argv[2]
    cutoff = int(sys.argv[3])
    
    sr, frames = wav.read(input_filename)
    l_channel = [frame[0] for frame in frames]
    r_channel = [frame[1] for frame in frames]

    l_channel_f = butter_lowpass_filter(l_channel, cutoff, sr)
    r_channel_f = butter_lowpass_filter(r_channel, cutoff, sr)

    # wav.write(output_filename, sr, np.asarray([[l, r] for l, r in
    #                                            zip(l_channel_f,
    #                                                r_channel_f)]))
    wav.write(output_filename, sr, l_channel_f)
