#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from six.move import xrange
from util import get_frame, read_signal


def itakura_saito_spectrum_distance(s, shat, winfunc):
    size = min(len(s), len(shat))
    window = winfunc(size)
    s = s[0:size]
    shat = shat[0:size]
    s_amp = np.absolute(np.fft.fftpack.fft(s * window))
    shat_amp = np.absolute(np.fft.fftpack.fft(shat * window))
    return np.mean(np.log(s_amp / shat_amp) + (shat_amp / s_amp) - 1.0)


def segmental_itakura_saito_spectrum_distance(s, shat, winsize, winfunc):
    size = min(len(s), len(shat))
    nf = size / (winsize / 2) - 1
    ret = []
    for no in xrange(nf):
        s_i = get_frame(s, winsize, no)
        shat_i = get_frame(shat, winsize, no)
        ret.append(itakura_saito_spectrum_distance(s_i, shat_i, winfunc))
    return ret


def log_spectrum_distance(s, shat, winfunc):
    size = min(len(s), len(shat))
    window = winfunc(size)
    s = s[0:size]
    shat = shat[0:size]
    s_amp = np.absolute(np.fft.fftpack.fft(s * window))
    shat_amp = np.absolute(np.fft.fftpack.fft(shat * window))
    return np.sqrt(np.mean((np.log10(s_amp / shat_amp) * 10.0) ** 2.0))


def segmental_log_spectrum_distance(s, shat, winsize, winfunc):
    size = min(len(s), len(shat))
    nf = size / (winsize / 2) - 1
    ret = []
    for no in xrange(nf):
        s_i = get_frame(s, winsize, no)
        shat_i = get_frame(shat, winsize, no)
        ret.append(log_spectrum_distance(s_i, shat_i, winfunc))
    return ret


if __name__ == "__main__":
    import sys
    winsize = int(sys.argv[1])
    s = read_signal(sys.argv[2], winsize)[0]
    shat = read_signal(sys.argv[3], winsize)[0]
    sissd = segmental_itakura_saito_spectrum_distance(s, shat, winsize, np.hanning)
    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(sissd)
    plt.show()
