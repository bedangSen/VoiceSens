#!/usr/bin/env python
# -*- coding: utf-8 -*-
#reference http://kaiseki-web.lhd.nifs.ac.jp/wiki/index.php/Python_%E3%81%AB%E3%82%88%E3%82%8B%E3%82%AA%E3%83%BC%E3%83%87%E3%82%A3%E3%82%AA%E5%87%A6%E7%90%86

import wave
import numpy as np
import scipy as sp
from six.moves import xrange, zip


def read_signal(filename, winsize):
    wf = wave.open(filename, 'rb')
    n = wf.getnframes()
    st = wf.readframes(n)
    params = ((wf.getnchannels(), wf.getsampwidth(),
               wf.getframerate(), wf.getnframes(),
               wf.getcomptype(), wf.getcompname()))
    siglen = ((int)(len(st) / 2 / winsize) + 1) * winsize
    signal = np.zeros(siglen, np.float32)
    signal[0:int(len(st) / 2)] = np.float32(np.fromstring(st, np.int16)) / 32767.0
    return [signal, params]


def get_frame(signal, winsize, no):
    shift = int(winsize / 2)
    start = int(no * shift)
    end = start + winsize
    return signal[start:end]


def add_signal(signal, frame, winsize, no):
    shift = int(winsize / 2)
    start = int(no * shift)
    end = start + winsize
    signal[start:end] = signal[start:end] + frame


def write_signal(filename, params, signal):
    wf = wave.open(filename, 'wb')
    wf.setparams(params)
    s = np.int16(signal * 32767.0).tostring()
    wf.writeframes(s)


def get_window(winsize, no):
    shift = int(winsize / 2)
    s = int(no * shift)
    return (s, s + winsize)


def separate_channels(signal):
    return signal[0::2], signal[1::2]


def uniting_channles(leftsignal, rightsignal):
    ret = []
    for i, j in zip(leftsignal, rightsignal):
        ret.append(i)
        ret.append(j)
    return np.array(ret, np.float32)


def compute_avgamplitude(signal, winsize, window):
    windownum = int(len(signal) / (winsize / 2)) - 1
    avgamp = np.zeros(winsize)
    for l in xrange(windownum):
        avgamp += np.absolute(sp.fft(get_frame(signal, winsize, l) * window))
    return avgamp / float(windownum)


def compute_avgpowerspectrum(signal, winsize, window):
    windownum = int(len(signal) / (winsize / 2)) - 1
    avgpow = np.zeros(winsize)
    for l in xrange(windownum):
        avgpow += np.absolute(sp.fft(get_frame(signal, winsize, l) * window))**2.0
    return avgpow / float(windownum)


def sigmoid(x, x0, k, a):
    y = k * 1 / (1 + np.exp(-a * (x - x0)))
    return y


def calc_kurtosis(samples):
    n = len(samples)
    avg = np.average(samples)
    moment2 = np.sum((samples - avg) ** 2) / n
    s_sd = np.sqrt(((n / (n - 1)) * moment2))
    k = ((n * (n + 1)) / ((n - 1) * (n - 2) * (n - 3))) * np.sum(((samples - avg) / s_sd) ** 4)
    return k - 3 * ((n - 1) ** 2) / ((n - 2) * (n - 3))
