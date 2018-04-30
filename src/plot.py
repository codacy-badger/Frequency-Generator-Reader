"""
 **File Name:** plot.py                                                                                               \n
 **Project:** CURRENTLY UNNAMED                                                                                       \n
 **Company:** Research in Flows, Inc                                                                                  \n
 **Author:** David Gurevich                                                                                           \n
 **Required Modules:**
       * numpy                                                                                                        \n
       * matplotlib.pyplot                                                                                            \n
       * peakutils                                                                                                    \n

This work is licensed under the Creative Commons Attribution-NonCommercial-NoDerivs 3.0 Unported License.
To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-nd/3.0/ or send a letter to
Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
"""

import matplotlib.pyplot as plt
import numpy as np
import peakutils

np.warnings.filterwarnings('ignore')


def determine_fq(fourier_transform, dur):
    indices = peakutils.indexes(fourier_transform, thres=0.)

    peaks = [fourier_transform[x] for x in indices]
    peaks.sort()

    # if peaks[0] == flat_fourier_transform[0]:
    #     peaks.pop(0)

    max_value_fft = peaks[-1]
    next_value_fft = peaks[-2]

    max_index = np.where(fourier_transform == max_value_fft)
    next_index = np.where(fourier_transform == next_value_fft)

    fq = ((max_index[0] - next_index[0])[0]) / dur
    return abs(fq), (max_index, max_value_fft), (next_index, next_value_fft)


def graph_input(signal, fs, fourier_transform, dur):
    fig_size = plt.rcParams["figure.figsize"]
    fig_size[0] = 6
    fig_size[1] = 9
    plt.rcParams["figure.figsize"] = fig_size

    x_r = np.arange(len(signal))
    y_r = signal

    plt.subplot(2, 1, 1)

    plt.plot(x_r, y_r, label="Received Signal")

    plt.xlabel('Point Number')
    plt.ylabel('Voltage (V)')
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)

    # PLOT 2
    plt.subplot(2, 1, 2)

    ts = 1.0/fs

    n = len(signal)
    k = np.arange(n)
    T = n/fs
    frq = k/T
    frq = np.array(frq[range(int(n / 2))])

    Y = fourier_transform/n
    Y = Y[range(int(n / 2))]

    plt.plot(frq, abs(Y), 'r')
    plt.xlabel('Freq (Hz)')
    plt.ylabel('Y(freq)')

    fq, max_vals, next_vals = determine_fq(fourier_transform, dur)
    plt.plot(max_vals[0], max_vals[1] / 100000, 'b+')
    plt.plot(next_vals[0], next_vals[1] / 100000, 'g+')
    print("Determined Frequency: ", fq)

    plt.savefig('Output/OutputPlot.png')
    plt.show()
