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

from ctypes import *

import numpy as np
import threading
import pickle
import pathlib


class Scanner(threading.Thread):
    def __init__(self, id, lib):
        threading.Thread.__init__(self)

        self.lib = lib

        # void scan(int** input, int rate, double dur) {}
        self.lib.scan.argtypes = [POINTER(POINTER(c_int)), c_int, c_double]
        self.lib.scan.restype = None

        # void release(int* input) {}
        self.lib.release.argtypes = [POINTER(c_int)]
        self.lib.release.restype = None

        self.rate = 4000000  # 8 MHz per Channel
        self.c_rate = c_int(self.rate)

        self.dur = 0.25  # x number of seconds
        self.c_dur = c_double(self.dur)

        self.p = POINTER(c_int)()

        self.len = int(2 * self.dur * self.rate)

        self.id = str(id)

    def run(self):
        self.lib.scan(self.p, self.c_rate, self.c_dur)
        self.collected_data = self.p


class Writer(threading.Thread):
    def __init__(self, scan_thread, id):
        threading.Thread.__init__(self)
        self.id = str(id)
        self.scan_thread = scan_thread

    def run(self):
        while True:
            if hasattr(self.scan_thread, 'collected_data'):
                self.to_write = np.fromiter(
                    self.scan_thread.p, dtype=np.int, count=self.scan_thread.len)
                self.scan_thread.lib.release(self.scan_thread.p)
                pickle.dump(self.to_write, open(
                    "Output/output" + self.id, "wb"))
                break


if __name__ == '__main__':
    count = 3

    threads = []
    lib = CDLL("src/scan.dll")
    pathlib.Path('Output').mkdir(parents=True, exist_ok=True)
    for i in range(count):
        threads.append(Scanner(i, lib))
        threads[-1].start()
        threads.append(Writer(threads[-1], i).start())

        scan_threads = threads[::2]
        for thread in scan_threads:
            thread.join()
