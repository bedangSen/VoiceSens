# -*- coding: utf-8 -*-
import numpy as np


class RecursiveAveragingEstimator:
    # http://www.sciencedirect.com/science/article/pii/S0167639305002001
    def __init__(self, winsize, window, samp_rate,
                 nu=0.7, B=0.8, gamma=0.998, alpha_p=0.2, alpha_d=0.85):

        def calc_delta():
            delta = np.zeros(winsize, dtype=np.float64)
            return delta

        self._window = window
        self._winsize = winsize
        # initial values
        frametime = (self._winsize / 2.0) / samp_rate  # frame incremental time [sec]
        self._snrexp = (-1.0) * frametime / 0.064
        self._av = 2.12

        self._nu = nu
        self._B = B
        self._gamma = gamma
        self._alpha_p = alpha_p
        self._alpha_d = alpha_d

        self._delta = calc_delta()

        self._nplist = []
        self._nsplist = []
        self._snsplist = []

    def init_noise_profile(self, NP):
        self._lastD = NP
        self._lastP = NP
        self._lastPmin = NP
        self._lastp = np.zeros(self._winsize, dtype=np.float64)

    def compute(self, frame, lamda):
        Y = np.fft.fftpack.fft(frame * self._window)
        Ysq = np.absolute(Y) ** 2.0
        return self.compute_with_power_spectrum(Ysq, lamda)

    def compute_with_power_spectrum(self, power_spectrum, lamda):
        Ysq = power_spectrum
        # Compute smooth speech power spectrum
        P = self._nu * self._lastP + (1.0 - self._nu) * Ysq  # eq 2

        # Find the local minimum of noisy speech
        Pmin = np.zeros(self._winsize, dtype=np.float64)
        minidx = np.less_equal(P, self._lastPmin)
        largeidx = np.greater(P, self._lastPmin)
        Pmin[minidx] = P[minidx]
        Pmin[largeidx] = self._gamma * self._lastPmin[largeidx] + \
                        ((1.0 - self._gamma) / (1.0 - self._B)) *\
                        (P[largeidx] - self._B * self._lastP[largeidx])  # eq3
        # Compute ratio of smoothed speech p
        Sr = P / Pmin  # eq4

        # Calculate speech presence probability using first-order recursion
        I = np.array(np.greater(self._delta, Sr), dtype=np.float64)  # eq5
        p = self._alpha_p * self._lastp + (1.0 - self._alpha_p) * I  # eq6

        # Compute time-frequency dependent smoothing factors
        alpha_s = self._alpha_d + (1.0 - self._alpha_d) * p  # eq7

        # Update noise estimate using time-frequency dependent smoothing factors
        D = alpha_s * self._lastD + (1.0 - alpha_s) * Ysq  # eq8

        # calculate debug info
        noise_periodgram = 10 * np.log10(np.sum(np.absolute(D)) / self._winsize)
        noisy_speech_periodgram = 10 * np.log10(np.sum(Ysq) / self._winsize)
        smooth_noisy_speech_periodgram = 10 * np.log10(np.sum(P) / self._winsize)
        self._nplist.append(noise_periodgram)
        self._nsplist.append(noisy_speech_periodgram)
        self._snsplist.append(smooth_noisy_speech_periodgram)
        # update
        self._lastP = P
        self._lastPmin = Pmin
        self._lastp = p
        self._lastD = D
        return D

    def show_debug_result(self):
        import matplotlib.pyplot as plt
        fig = plt.figure()

        ax = fig.add_subplot(111)

        ax.grid('on', 'major', color='#666666', linestyle='-')

        ax.plot(self._nsplist)
        ax.plot(self._snsplist, linewidth=3.0)
        ax.plot(self._nplist, linewidth=3.0)
        ax.legend(("Periodgram", "Smoothed Periodgram", "Estimated Noise"))  # ,"True Noise"))
        plt.show()
