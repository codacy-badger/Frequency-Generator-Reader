"""
 **File Name:** util.py                                                                                               \n
 **Project:** CURRENTLY UNNAMED                                                                                       \n
 **Company:** Research in Flows, Inc                                                                                  \n
 **Author:** David A. Gurevich                                                                                        \n
 **Required Modules:**
       * numpy                                                                                                        \n
       * matplotlib.pyplot                                                                                            \n
       * peakutils                                                                                                    \n

Frequency-Generator Reader | Local software for generating and processing high-frequency signals
Copyright (C) 2018  David A. Gurevich

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import matplotlib.pyplot as plt
import numpy as np
import peakutils

np.warnings.filterwarnings('ignore')


def determine_fq(fourier_transform, dur):
    flat_fourier_transform = fourier_transform.flatten()

    indices = peakutils.indexes(flat_fourier_transform, thres=0.)

    peaks = [flat_fourier_transform[x] for x in indices]
    peaks.sort()

    if peaks[0] == flat_fourier_transform[0]:
        peaks.pop(0)

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
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
               ncol=2, mode="expand", borderaxespad=0.)

    # PLOT 2
    plt.subplot(2, 1, 2)

    ts = 1.0 / fs

    n = len(signal)
    k = np.arange(n)
    T = n / fs
    frq = k / T
    frq = np.array(frq[range(int(n / 2))])

    Y = fourier_transform / n
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
