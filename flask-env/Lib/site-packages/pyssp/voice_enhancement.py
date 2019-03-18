#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import scipy.special as spc
from pyssp.util import sigmoid
from six.moves import xrange


class SpectralSubtruction(object):
    def __init__(self, winsize, window, coefficient=5.0, ratio=1.0):
        self._window = window
        self._coefficient = coefficient
        self._ratio = ratio

    def compute(self, signal, noise):
        n_spec = np.fft.fftpack.fft(noise * self._window)
        n_pow = np.absolute(n_spec) ** 2.0
        return self.compute_by_noise_pow(signal, n_pow)

    def compute_by_noise_pow(self, signal, n_pow):
        s_spec = np.fft.fftpack.fft(signal * self._window)
        s_amp = np.absolute(s_spec)
        s_phase = np.angle(s_spec)
        amp = s_amp ** 2.0 - n_pow * self._coefficient
        amp = np.maximum(amp, 0.0)
        amp = np.sqrt(amp)
        amp = self._ratio * amp + (1.0 - self._ratio) * s_amp
        spec = amp * np.exp(s_phase * 1j)
        return np.real(np.fft.fftpack.ifft(spec))


class SpectrumReconstruction(object):
    def __init__(self, winsize, window, constant=0.001, ratio=1.0, alpha=0.99):
        self._window = window
        self._G = np.zeros(winsize, np.float64)
        self._prevGamma = np.zeros(winsize, np.float64)
        self._alpha = alpha
        self._prevAmp = np.zeros(winsize, np.float64)
        self._ratio = ratio
        self._constant = constant

    def _sigmoid(self, gain):
        for i in xrange(len(gain)):
            gain[i] = sigmoid(gain[1], 1, 2, self._gain)

    def compute(self, signal, noise):
        n_spec = np.fft.fftpack.fft(noise * self._window)
        n_pow = np.absolute(n_spec) ** 2.0
        return self.compute_by_noise_pow(signal, n_pow)

    def _calc_aposteriori_snr(self, s_amp, n_pow):
        return s_amp ** 2.0 / n_pow

    def _calc_apriori_snr(self, gamma):
        return self._alpha * self._G ** 2.0 * self._prevGamma +\
            (1.0 - self._alpha) * np.maximum(gamma - 1.0, 0.0)  # a priori s/n ratio

    def _calc_apriori_snr2(self, gamma, n_pow):
        return self._alpha * (self._prevAmp ** 2.0 / n_pow) +\
            (1.0 - self._alpha) * np.maximum(gamma - 1.0, 0.0)  # a priori s/n ratio


class MMSE_STSA(SpectrumReconstruction):
    def __init__(self, winsize, window, constant=0.001, ratio=1.0, alpha=0.99):
        self._gamma15 = spc.gamma(1.5)
        super(MMSE_STSA, self).__init__(winsize, window, constant=constant, ratio=ratio, alpha=alpha)

    def compute_by_noise_pow(self, signal, n_pow):
        s_spec = np.fft.fftpack.fft(signal * self._window)
        s_amp = np.absolute(s_spec)
        s_phase = np.angle(s_spec)
        gamma = self._calc_aposteriori_snr(s_amp, n_pow)
        xi = self._calc_apriori_snr(gamma)
        self._prevGamma = gamma
        nu = gamma * xi / (1.0 + xi)
        self._G = (self._gamma15 * np.sqrt(nu) / gamma) * np.exp(-nu / 2.0) *\
                  ((1.0 + nu) * spc.i0(nu / 2.0) + nu * spc.i1(nu / 2.0))
        idx = np.less(s_amp ** 2.0, n_pow)
        self._G[idx] = self._constant
        idx = np.isnan(self._G) + np.isinf(self._G)
        self._G[idx] = xi[idx] / (xi[idx] + 1.0)
        idx = np.isnan(self._G) + np.isinf(self._G)
        self._G[idx] = self._constant
        self._G = np.maximum(self._G, 0.0)
        amp = self._G * s_amp
        amp = np.maximum(amp, 0.0)
        amp2 = self._ratio * amp + (1.0 - self._ratio) * s_amp
        self._prevAmp = amp
        spec = amp2 * np.exp(s_phase * 1j)
        return np.real(np.fft.fftpack.ifft(spec))


class MMSE_LogSTSA(SpectrumReconstruction):
    def __init__(self, winsize, window, constant=0.001, ratio=1.0, alpha=0.99):
        self._gamma15 = spc.gamma(1.5)
        super(MMSE_LogSTSA, self).__init__(winsize, window, constant=constant, ratio=ratio, alpha=alpha)

    def compute_by_noise_pow(self, signal, n_pow):
        s_spec = np.fft.fftpack.fft(signal * self._window)
        s_amp = np.absolute(s_spec)
        s_phase = np.angle(s_spec)
        gamma = self._calc_aposteriori_snr(s_amp, n_pow)
        xi = self._calc_apriori_snr(gamma)
        # xi = self._calc_apriori_snr2(gamma,n_pow)
        self._prevGamma = gamma
        nu = gamma * xi / (1.0 + xi)
        self._G = xi / (1.0 + xi) * np.exp(0.5 * spc.exp1(nu))
        idx = np.less(s_amp ** 2.0, n_pow)
        self._G[idx] = self._constant
        idx = np.isnan(self._G) + np.isinf(self._G)
        self._G[idx] = xi[idx] / (xi[idx] + 1.0)
        idx = np.isnan(self._G) + np.isinf(self._G)
        self._G[idx] = self._constant
        self._G = np.maximum(self._G, 0.0)
        amp = self._G * s_amp
        amp = np.maximum(amp, 0.0)
        amp2 = self._ratio * amp + (1.0 - self._ratio) * s_amp
        self._prevAmp = amp
        spec = amp2 * np.exp(s_phase * 1j)
        return np.real(np.fft.fftpack.ifft(spec))


class JointMap(SpectrumReconstruction):
    def __init__(self, winsize, window, constant=0.001, ratio=1.0, alpha=0.99, mu=1.74, tau=0.126):
        self._mu = mu
        self._tau = tau
        super(JointMap, self).__init__(winsize, window, constant=constant, ratio=ratio, alpha=alpha)

    def compute_by_noise_pow(self, signal, n_pow):
        s_spec = np.fft.fftpack.fft(signal * self._window)
        s_amp = np.absolute(s_spec)
        s_phase = np.angle(s_spec)
        gamma = self._calc_aposteriori_snr(s_amp, n_pow)
        # xi = self._calc_apriori_snr2(gamma,n_pow)
        xi = self._calc_apriori_snr(gamma)
        self._prevGamma = gamma
        u = 0.5 - self._mu / (4.0 * np.sqrt(gamma * xi))
        self._G = u + np.sqrt(u ** 2.0 + self._tau / (gamma * 2.0))
        idx = np.less(s_amp ** 2.0, n_pow)
        self._G[idx] = self._constant
        idx = np.isnan(self._G) + np.isinf(self._G)
        self._G[idx] = xi[idx] / (xi[idx] + 1.0)
        idx = np.isnan(self._G) + np.isinf(self._G)
        self._G[idx] = self._constant
        self._G = np.maximum(self._G, 0.0)
        amp = self._G * s_amp
        amp = np.maximum(amp, 0.0)
        amp2 = self._ratio * amp + (1.0 - self._ratio) * s_amp
        self._prevAmp = amp
        spec = amp2 * np.exp(s_phase * 1j)
        return np.real(np.fft.fftpack.ifft(spec))
