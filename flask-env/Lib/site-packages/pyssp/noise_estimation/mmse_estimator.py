# -*- coding: utf-8 -*-
import numpy as np


class MMSEEstimator:
    # ieeexplore.ieee.org/xpls/abs_all.jsp?arnumber=6111268
    def __init__(self, winsize, window):
        self._winsize = winsize
        self._window = window
        self._alpha_ph1_mean = 0.9
        self._alpha_psd = 0.8
        self._q = 0.5
        self._prior_fact = self._q / (1 - self._q)
        self._xi_opt_db = 30.0
        self._xi_opt = 10.0 ** (self._xi_opt_db / 10.0)
        self._log_glr_fact = np.log(1.0 / (1.0 + self._xi_opt_db))
        self._glr_exp = self._xi_opt / (1.0 + self._xi_opt)

        self._ph1_mean = np.zeros(self._winsize) + 0.5

    def init_noise_profile(self, noise_pow):
        self._noise_pow = noise_pow

    def compute(self, frame):
        spec = np.fft.fftpack.fft(frame * self._window)
        power = np.absolute(spec) ** 2
        return self.compute_with_power_spectrum(power)

    def compute_with_power_spectrum(self, noisy_per):
        snr_post1 = noisy_per / self._noise_pow
        glr = self._prior_fact * np.exp(np.minimum(self._log_glr_fact + self._glr_exp * snr_post1, 200))
        ph1 = glr / (1.0 + glr)

        self._ph1_mean = self._alpha_ph1_mean * self._ph1_mean + (1.0 - self._alpha_ph1_mean) * ph1
        idxs = self._ph1_mean > 0.99
        ph1[idxs] = np.minimum(ph1[idxs], 0.99)
        estimate = ph1 * self._noise_pow + (1.0 - ph1) * noisy_per
        self._noise_pow = self._alpha_psd * self._noise_pow + (1.0 - self._alpha_psd) * estimate
        return self._noise_pow
