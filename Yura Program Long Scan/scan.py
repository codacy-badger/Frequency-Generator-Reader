"""
 **File Name:** scan.py                                                                                               \n
 **Project:** CURRENTLY UNNAMED                                                                                       \n
 **Company:** Research in Flows, Inc                                                                                  \n
 **Author:** David Gurevich                                                                                           \n
 **Required Modules:**
       * numpy                                                                                                        \n

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

from mcculw import ul
from mcculw.enums import ULRange

from ctypes import *

import numpy as np


def scan():
    lib = CDLL('src/scan.dll')

    # void scan(int** input, int rate, int dur) {}
    lib.scan.argtypes = [POINTER(POINTER(c_int)), c_int, c_int]
    lib.scan.restype = None

    # void release(int* input) {}
    lib.release.argtypes = [POINTER(c_int)]
    lib.release.restype = None

    rate = 8000000  # 8 MHz - Maxiumum scan rate for non-BURSTIO
    c_rate = c_int(rate)

    dur = 10  # 10 seconds - Completely arbitrary number
    c_dur = c_int(dur)

    daq_data = np.array(np.zeroes(rate * dur))
    p = POINTER(c_int)()
    lib.scan(p, c_rate, c_dur)
    for i in range(len(p)):
        daq_data[i] = (ul.to_eng_units(0, ULRange.BIP1BIP1VOLTS, p[i]))

    lib.release(p)

    print("Scan and Convert complete!")

    for i in range(len(daq_data)):
        print(i, ": ", daq_data[i])

scan()
