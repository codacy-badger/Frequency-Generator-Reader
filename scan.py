"""
 **File Name:** scan.py                                                                                               \n
 **Project:** CURRENTLY UNNAMED                                                                                       \n
 **Company:** Research in Flows, Inc                                                                                  \n
 **Author:** David Gurevich                                                                                           \n
 **Required Modules:**
       * numpy                                                                                                        \n
       * matplotlib                                                                                                   \n
	   * keyboard																									  \n

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

from ctypes import *

import keyboard
import numpy as np
import matplotlib.pyplot as plt


def scan():
    lib = CDLL('src/scan.dll')

    # void scan(int** input, int rate, int dur) {}
    lib.scan.argtypes = [POINTER(POINTER(c_int)), c_int, c_float]
    lib.scan.restype = None

    # void release(int* input) {}
    lib.release.argtypes = [POINTER(c_int)]
    lib.release.restype = None

    rate = 20000000  # x Hz or x / 10e6 MHz | Maxiumum scan rate for non-BURSTIO
    c_rate = c_int(rate)

    dur = 0.05  # x number of seconds - Completely arbitrary number
    c_dur = c_float(dur)

    total_data = []
    p = POINTER(c_int)()

    for i in range(5):
        lib.scan(p, c_rate, c_dur)
        total_data.extend(np.fromiter(p, dtype=np.int, count=int(2*dur*rate)))
        lib.release(p)

    plt.plot(total_data[::2])
    plt.plot(total_data[1::2])
    plt.show()


if __name__ == '__main__':
    scan()
