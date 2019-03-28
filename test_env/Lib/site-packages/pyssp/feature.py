#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from statsmodels.tsa.stattools import acf
from six.moves import xrange
from pyssp.utils import calc_kurtosis


def levinson_durbin(r, order):
    """
    from http://aidiary.hatenablog.com/entry/20120415/1334458954
    """
    a = np.zeros(order + 1)
    e = np.zeros(order + 1)

    # k = 1
    a[0] = 1.0
    a[1] = - r[1] / r[0]
    e[1] = r[0] + r[1] * a[1]
    lam = - r[1] / r[0]

    for k in xrange(1, order):
        # update lambda
        lam = 0.0
        for j in xrange(k + 1):
            lam -= a[j] * r[k + 1 - j]
        lam /= e[k]

        # update a with U and V
        U = [1]
        U.extend([a[i] for i in xrange(1, k + 1)])
        U.append(0)
        V = [0]
        V.extend([a[i] for i in xrange(k, 0, -1)])
        V.append(1)
        a = np.array(U) + lam * np.array(V)

        # update e
        e[k + 1] = e[k] * (1.0 - lam * lam)

    return a, e[-1]


def lpc(frame, order):
    """
    frame: windowed signal
    order: lpc order
    return from 0th to `order`th linear predictive coefficients
    """
    r = acf(frame, unbiased=False, nlags=order)
    return levinson_durbin(r, order)[0]


def lpr_kurtosis(frame, lpcorder=10):
    """
    frame: windowed signal
    return kurtosis of linear prediction residual from input signal
    """
    c = lpc(frame, lpcorder)
    coef = c[1:][::-1] * -1
    residuals = []
    for i in xrange(frame.size - 10):
        residuals.append(frame[i + 10] - np.sum(frame[i:i + 10] * coef))
    residuals = np.array(residuals)
    return calc_kurtosis(residuals)
