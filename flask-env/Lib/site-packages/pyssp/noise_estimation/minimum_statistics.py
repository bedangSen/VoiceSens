# -*- coding: utf-8 -*-
import scipy as sp
import numpy as np


# compute smoothing parameter
def M_H(D):
    if(D == 1):
        M = 0
        H = 0
    elif(D == 2):
        M = 0.26
        H = 0.15
    elif(D == 4):
        # nodata
        M = 0.40
        H = 0.30
    elif(D == 5):
        M = 0.48
        H = 0.48
    elif(D == 6):
        # nodata
        M = 0.50
        H = 0.65
    elif(D == 8):
        M = 0.58
        H = 0.78
    elif(D == 10):
        M = 0.61
        H = 0.98
    elif(D == 12):
        M = 0.64
        H = 1.25
    elif(D == 15):
        M = 0.668
        H = 1.55
    elif(D == 18):
        # nodata
        M = 0.68
        H = 1.7
    elif(D == 20):
        M = 0.705
        H = 2.0
    elif(D == 24):
        # no data
        M = 0.730
        H = 2.15
    elif(D == 30):
        M = 0.762
        H = 2.3
    elif(D == 40):
        M = 0.8
        H = 2.52
    elif(D == 60):
        M = 0.841
        H = 2.52
    elif(D == 80):
        M = 0.865
        H = 3.25
    elif(D == 96):
        M = 0.87
        H = 3.5
    elif(D == 120):
        M = 0.89
        H = 4.0
    elif(D == 140):
        M = 0.9
        H = 4.1
    elif(D == 160):
        M = 0.91
        H = 4.1
    elif(D == 192):
        # nodata
        M = 0.92
        H = 4.2
    else:
        M = -1
        H = -1
        print("D value:", D)
        raise ValueError('D out of range')
    return M, H


class MinimumStatistics():

    def __init__(self, winsize, window, samp_rate):
        self._window = window
        self._winsize = winsize

        # initial values
        frametime = (self._winsize / 2.0) / samp_rate  # frame incremental time [sec]
        self._snrexp = (-1.0) * frametime / 0.064
        self._av = 2.12

        self._alpha_c_lambda = 0.7
        # U subwindows
        self._U = 8
        # V samples
        self._V = 12
        # D window (96 samples)
        self._D = self._U * self._V
        self._subwc = self._V - 1
        self._ibuf = 0
        self._lmin_flag_lambda = np.zeros(self._winsize)
        self._alpha_max = 0.96
        self._beta_max = 0.8

        qeqmax = 14.0  # max value of Qeq per frame
        self._qeqimin = 1 / qeqmax

        self._clear_max = 65535 * 65535
        self._actmin_lambda = np.ones(self._winsize)
        self._actmin_lambda = self._actmin_lambda * self._clear_max
        self._actmin_lambda_sub = self._actmin_lambda
        self._Pmin_u_lambda = self._actmin_lambda
        self._actbuf = np.ones((self._U, self._winsize))
        self._actbuf = self._actbuf * self._clear_max

        # for graph
        self._x_data = []
        self._y_data = []
        self._p_data = []
        self._x_data_all = []
        self._y_data_all = []
        self._p_data_all = []
        pass

    def init_noise_profile(self, NP_lambda):
        self._P_lambda = NP_lambda
        self._sn2_lambda = self._P_lambda
        self._eP_lambda = self._P_lambda
        self._eP2_lambda = self._eP_lambda ** 2
        self._Pmin_u_lambda = self._P_lambda

    def compute(self, frame, lamda):
        Y_lambda = np.fft.fftpack.fft(frame * self._window)
        power = np.absolute(Y_lambda) ** 2
        return self.compute_with_power_spectrum(power, lamda)

    def compute_with_power_spectrum(self, power_spectrum, lamda):
        # eq9
        alpha_c_lambda_tilde = 1.0 / (1.0 + (np.sum(self._P_lambda) / np.sum(power_spectrum) - 1.0) ** 2)
        # eq10
        self._alpha_c_lambda = 0.7 * self._alpha_c_lambda + 0.3 * np.maximum(alpha_c_lambda_tilde, 0.7)
        # eq11
        alpha_lambda_hat = (self._alpha_max * self._alpha_c_lambda) / (1 + (self._P_lambda / self._sn2_lambda - 1) ** 2)
        # eq12
        snr = np.sum(self._P_lambda) / np.sum(self._sn2_lambda)
        alpha_lambda_hat = np.maximum(alpha_lambda_hat, np.minimum(0.3, snr ** self._snrexp))
        # eq4 smoothed periodgram
        self._P_lambda = alpha_lambda_hat * self._P_lambda + (1.0 - alpha_lambda_hat) * power_spectrum
        # eq20
        beta_lambda = np.minimum(alpha_lambda_hat ** 2, self._beta_max)
        self._eP_lambda = beta_lambda * self._eP_lambda + (1.0 - beta_lambda) * self._P_lambda
        self._eP2_lambda = beta_lambda * self._eP2_lambda + (1.0 - beta_lambda) * (self._P_lambda ** 2)
        # eq22
        vP_lambda = self._eP2_lambda - (self._eP_lambda ** 2)
        # eq23 modification
        Qeq_lambda_inverse = np.maximum(np.minimum(vP_lambda / (2 * (self._sn2_lambda ** 2)), 0.5),
                                        self._qeqimin / (lamda + 1))

        # eq23 + 12 lines
        eQ_lambda = np.sum(Qeq_lambda_inverse) / self._winsize
        # eq23 + 11 lines
        Bc_lambda = 1.0 + self._av * np.sqrt(eQ_lambda)

        # ----------------------------------------------------------------------------------------
        # for overall window of length D
        # ----------------------------------------------------------------------------------------

        # eq16
        M, H = M_H(self._D)
        Qeq_lambda_tilde = (1.0 / Qeq_lambda_inverse - 2 * M) / (1 - M)
        # eq17
        Bmin_lambda = 1.0 + (self._D - 1) * 2.0 / Qeq_lambda_tilde

        # ----------------------------------------------------------------------------------------
        # for subwindow U of length V
        # ----------------------------------------------------------------------------------------

        # eq16
        M, H = M_H(self._V)
        Qeq_lambda_tilde_sub = (1.0 / Qeq_lambda_inverse - 2 * M) / (1 - M)
        # eq17
        Bmin_lambda_sub = 1.0 + (self._V - 1) * 2.0 / Qeq_lambda_tilde_sub

        # ----------------------------------------------------------------------------------------

        # set k_mod(k) = 0 for all frequency bin k
        k_mod = np.zeros(self._winsize)

        # calc actmin
        actmin_lambda_current = self._P_lambda * Bmin_lambda * Bc_lambda
        # if(P*Bmin*Bc < actmin)
        k_mod = np.less(actmin_lambda_current, self._actmin_lambda)
        if(k_mod.any()):
            # update new minimum of D
            self._actmin_lambda[k_mod] = actmin_lambda_current[k_mod]
            # update new minimum of V
            actmin_lambda_current_sub = self._P_lambda * Bmin_lambda_sub * Bc_lambda
            self._actmin_lambda_sub[k_mod] = actmin_lambda_current_sub[k_mod]

        if(0 < self._subwc and self._subwc < self._V - 1):
            # sample is NOT the fisrt or the last; middle of buffer allows a local minimum
            self._lmin_flag_lambda = np.minimum(self._lmin_flag_lambda + k_mod, 1)
            # calc Pmin_u_lamda == sigma_n_lamda_hat**2
            self._Pmin_u_lambda = np.minimum(self._actmin_lambda_sub, self._Pmin_u_lambda)
            # store sn2 for later use
            self._sn2_lambda = self._Pmin_u_lambda
            self._subwc = self._subwc + 1
        elif(self._subwc >= self._V - 1):
            # sample IS the last; end of buffer lets finishing subwindow process and a buffer switch
            self._lmin_flag_lambda = np.maximum(self._lmin_flag_lambda - k_mod, 0)
            # store actmin_lamnda, note actbuf is NOT cyclic!
            self._ibuf = np.mod(self._ibuf, self._U)
            self._actbuf[self._ibuf] = self._actmin_lambda
            self._ibuf = self._ibuf + 1
            # find Pmin_u, the minimum of the last U stored value of actmin
            self._Pmin_u_lambda = self._actbuf.min(axis=0)

            # calc noise_slope_max
            if(eQ_lambda < 0.03):
                noise_slope_max = 8.0
            elif(eQ_lambda < 0.05):
                noise_slope_max = 4.0
            elif(eQ_lambda < 0.06):
                noise_slope_max = 2.0
            else:
                noise_slope_max = 1.2
            # replace all previously stored values of actmin by actminsub
            lmin = self._lmin_flag_lambda * np.less(self._actmin_lambda_sub,
                                                    noise_slope_max * self._Pmin_u_lambda) *\
                  np.less(self._Pmin_u_lambda, self._actmin_lambda_sub)
            lmin = np.int16(lmin)
            if(lmin.any()):
                self._Pmin_u_lambda[lmin] = self._actmin_lambda_sub[lmin]
                r = np.ones((self._U, self._winsize))
                rp = r * self._Pmin_u_lambda
                self._actbuf[:, lmin] = rp[:, lmin]

            # update flags
            self._lmin_flag_lambda = np.zeros(self._winsize)
            self._actmin_lambda = np.ones(self._winsize) * self._clear_max
            self._subwc = 0
        else:
            self._subwc = self._subwc + 1

        x = self._sn2_lambda
        # stderror; paper [2], Fig 15; not use
        # qisq = np.sqrt(Qeq_lambda_inverse)
        # xs = x*np.sqrt(0.266*(self._D+100*qisq)*qisq/\
        # (1+0.005*self._D+6.0/self._D)/(0.5*(1.0/Qeq_lambda_inverse)+self._D-1))
        self._x_data.append(x)

        self._x_data_all.append(10 * np.log10(np.sum(np.absolute(x)) / self._winsize))
        self._p_data_all.append(10 * np.log10(np.sum(self._P_lambda) / self._winsize))
        self._y_data.append(power_spectrum)
        self._y_data_all.append(10 * np.log10(np.sum(power_spectrum) / self._winsize))
        return x

    def show_debug_result(self):
        import matplotlib.pyplot as plt
        fig = plt.figure()

        ax = fig.add_subplot(111)

        ax.grid('on', 'major', color='#666666', linestyle='-')

        ax.plot(self._y_data_all)
        ax.plot(self._p_data_all, linewidth=3.0)
        ax.plot(self._x_data_all, linewidth=3.0)
        ax.legend(("Periodgram", "Smoothed Periodgram", "Estimated Noise"))  # ,"True Noise"))
        plt.show()
