"""
 **File Name:** test_scan_position.py                                                                                 \n
 **Project:** CURRENTLY UNNAMED                                                                                       \n
 **Company:** Research in Flows, Inc                                                                                  \n
 **Author:** David A. Gurevich                                                                                        \n
 **Required Modules:**                                                                                                \n
       * numpy                                                                                                        \n
       * HantekDDS                                                                                                    \n

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
import numpy as np
import hantekdds.htdds_wrapper as hantekdds
import matplotlib.pyplot as plt

import ctypes

FUNCTION_GENERATOR = hantekdds.HantekDDS()
FUNCTION_GENERATOR.drive_periodic(frequency=120000.0)


def run_scan():
    lib = ctypes.CDLL('src/scan.dll')

    lib.scan.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_int)), ctypes.c_int, ctypes.c_double]
    lib.scan.restype = None

    lib.release.argtypes = [ctypes.POINTER(ctypes.c_int)]
    lib.release.restype = None

    rate = 16000000
    c_rate = ctypes.c_int(rate)

    dur = 0.00005
    c_dur = ctypes.c_double(dur)

    p = ctypes.POINTER(ctypes.c_int)()
    arr_len = int(2 * dur * rate)

    lib.scan(p, c_rate, c_dur)

    arr = np.fromiter(p, dtype=np.int, count=arr_len)
    return arr


if __name__ == '__main__':
    while True:
        plt.clf()
        plt.plot(run_scan()[::2])
        plt.pause(0.00005)
