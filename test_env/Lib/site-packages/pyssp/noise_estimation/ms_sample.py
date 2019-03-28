# -*- coding: utf-8 -*-
import wave
import scipy as sp
from util import read_signal, get_frame, add_signal, write_signal, compute_avgpowerspectrum
from pyssp.voice_enhancement import JointMap
from six.move import xrange
from .MinimumStatistics import MinimumStatistics

if __name__ == "__main__":
    WINSIZE = 512
    samplingrate = 16000
    chunk = 1024
    soundfile = 'tools/sound/F2AKFU.SD.E03.16k.2.wav'
    soundfile = 'tools/sound/b01.wav'
    noisefile = 'tools/sound/air_vent.16k.wav'
    sound = wave.open(soundfile, 'rb')
    noise = wave.open(noisefile, 'rb')

    synthfile = 'tools/sound/noisy.wav'
    synth = wave.open(synthfile, 'wb')
    synth.setnchannels(1)
    synth.setsampwidth(2)
    synth.setframerate(samplingrate)

    remain = sound.getnframes()

    while remain > 0:
        s = min(chunk, remain)
        # read frames
        data_sound = sound.readframes(s)
        data_noise = noise.readframes(s)
        # convert
        ary_sound = sp.fromstring(data_sound, sp.int16)
        ary_noise = sp.fromstring(data_noise, sp.int16)

        int32_ary_sound = sp.int32(ary_sound)
        int32_ary_noise = sp.int32(ary_noise)
        ary2 = sp.int16(int32_ary_sound + int32_ary_noise)
        data2 = ary2.tostring()
        synth.writeframes(data2)
        remain = remain - s
    sound.close()
    noise.close()
    synth.close()

    infile = 'tools/sound/noisy.wav'
    signal, params = read_signal(infile, WINSIZE)
    nf = len(signal) / (WINSIZE / 2) - 1
    sig_out = sp.zeros(len(signal), sp.float32)
    window = sp.hanning(WINSIZE)

    ms = MinimumStatistics(WINSIZE, window, params[2])
    NP_lambda = compute_avgpowerspectrum(signal[0:WINSIZE * int(params[2] / float(WINSIZE) / 3.0)],
                                         WINSIZE, window)
    ms.init_noise_profile(NP_lambda)
    ss = JointMap(WINSIZE, window)
    for no in xrange(nf):
        frame = get_frame(signal, WINSIZE, no)
        n_pow = ms.compute(frame, no)
        res = ss.compute_by_noise_pow(frame, n_pow)
        add_signal(sig_out, res, WINSIZE, no)

    ms.show_debug_result()
    write_signal("tools/sound/noise_reduction.wav", params, sig_out)
