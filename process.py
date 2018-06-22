"""
 **File Name:** process.py                                                                        \n
 **Project:** CURRENTLY UNNAMED                                                                   \n
 **Company:** Research in Flows, Inc                                                              \n
 **Author:** David A. Gurevich                                                                    \n
 **Required Modules:**
       * matplotlib                                                                               \n

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

from mcculw import ul
from mcculw.enums import ULRange

from matplotlib import pyplot as plt


if __name__ == '__main__':
    DATA = []
    PATH, DIRS, FILES = next(os.walk("Output"))
    FILE_COUNT = len(FILES)
    for i in range(FILE_COUNT):
        str_i = str(i)
        with open('Output/output' + str_i + '.bin', 'rb') as fp:
            to_add = pickle.load(fp)
            DATA.extend(to_add)

    DATA = [ul.to_eng_units(0, ULRange.BIP1VOLTS, int(i)) for i in DATA]
    CHAN1 = DATA[::2]
    CHAN2 = DATA[1::2]

    plt.plot(CHAN1)
    plt.plot(CHAN2)
    plt.show()
