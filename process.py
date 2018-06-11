"""
 **File Name:** process.py                                                                                            \n
 **Project:** CURRENTLY UNNAMED                                                                                       \n
 **Company:** Research in Flows, Inc                                                                                  \n
 **Author:** David Gurevich                                                                                           \n
 **Required Modules:**
       * matplotlib                                                                                                   \n

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

import pickle
import os

from src.util import determine_fq

from mcculw import ul
from mcculw.enums import ULRange
from mcculw.ul import ULError

import numpy as np

from matplotlib import pyplot as plt


if __name__ == '__main__':
    data = []
    path, dirs, files = next(os.walk("Output"))
    file_count = len(files)
    for i in range(file_count):
        str_i = str(i)
        with open('Output/output' + str_i + '.bin', 'rb') as fp:
            to_add = pickle.load(fp)
            data.extend(to_add)

    data = [ul.to_eng_units(0, ULRange.BIP1VOLTS, int(i)) for i in data]
    chan1 = data[::2]
    chan2 = data[1::2]

    plt.plot(chan1)
    plt.plot(chan2)
    plt.show()
