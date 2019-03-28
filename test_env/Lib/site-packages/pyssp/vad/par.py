# -*- coding: utf-8 -*-
import scipy as sp
import numpy as np


def calc_nullhypotes(pa, pp, alpha=1.0):
    return (1.0 / (np.sqrt(np.pi * 2) * alpha * pa)) * np.exp((-1.0 / 2 * (alpha ** 2)) * (pp / pa) ** 2)


def calc_hypotes(pa, pp, beta=1.0):
    return (1.0 / (np.sqrt(np.pi * 2) * beta * pp)) * np.exp((-1.0 / 2 * (beta ** 2)) * (pa / pp) ** 2)


class PAR:
    def __init__(self, winsize, window, alpha=1.0, beta=1.0):
        self._winsize = winsize
        self._window = window
        self._alpha = alpha
        self._beta = beta
        self._eta = (2.0 * (window ** 2).sum()) / window.sum() ** 2

    def calc_par(self, frame):
        power = sp.absolute(sp.fft(frame * self._window)) ** 2
        avg_pow = power[:int(self._winsize / 2)].sum() / (self._winsize / 2)
        smax = -np.inf
        lenmax = 0
        for i in range(2, int(self._winsize / 10)):
            # searching f0 with maximizing estimated power of periodic component
            idx = list(range(i, int(self._winsize / 2), i + 1))
            score = power[:int(self._winsize / 2)][idx].sum() - (len(idx) * avg_pow)
            if score > smax:
                smax = score
                lenmax = len(idx)
        pp = (smax / (1.0 - self._eta * lenmax)) * self._eta
        pa = avg_pow - pp
        return calc_hypotes(pa, pp, beta=self._beta) / calc_nullhypotes(pa, pp, alpha=self._alpha)

    
