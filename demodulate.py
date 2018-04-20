"""
 **File Name:** demodulate.py                                                                                         \n
 **Project:** CURRENTLY UNNAMED                                                                                       \n
 **Company:** Research in Flows, Inc                                                                                  \n
 **Author:** David Gurevich                                                                                           \n
 **Required Modules:**
       * numpy                                                                                                        \n
       * scipy                                                                                                        \n

This work is licensed under the Creative Commons Attribution-NonCommercial-NoDerivs 3.0 Unported License.
To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-nd/3.0/ or send a letter to
Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
"""

import numpy as np
from scipy.signal import hilbert, medfilt


def hilbert_envelope(duration, fs, signal, acc):
    samples = int(fs*duration)
    signal_length = len(signal)

    analytic_signal = hilbert(signal)
    print("Completed Hilbert transformation")
    amplitude_envelope = np.abs(analytic_signal)
    # instantaneous_phase = np.unwrap(np.angle(analytic_signal))
    # instantaneous_frequency = (np.diff(instantaneous_phase) / (2.0*np.pi) * fs)

    if signal_length % acc == 0:
        kernel_size = int(signal_length/acc) - 1
    else:
        kernel_size = int(signal_length/acc)

    while True:
        try:
            fil_amplitude_envelope = medfilt(amplitude_envelope, kernel_size)
            break
        except ValueError:
            kernel_size += 1

    return (analytic_signal, amplitude_envelope, fil_amplitude_envelope)
