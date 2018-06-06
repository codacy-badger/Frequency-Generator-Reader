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

import pathlib
import pickle
import sys
import threading
from ctypes import *

import numpy as np


class Scanner(threading.Thread):
    def __init__(self, iteration, dll_lib):
        threading.Thread.__init__(self)

        self.lib = dll_lib

        # void scan(int** input, int rate, double dur) {}
        self.lib.scan.argtypes = [POINTER(POINTER(c_int)), c_int, c_double]
        self.lib.scan.restype = None

        # void release(int* input) {}
        self.lib.release.argtypes = [POINTER(c_int)]
        self.lib.release.restype = None

        self.rate = 20000000  # 20 MHz per Channel
        self.c_rate = c_int(self.rate)

        self.dur = 0.1  # x number of seconds
        self.c_dur = c_double(self.dur)

        self.P = POINTER(c_int)()
        self.len = int(2 * self.dur * self.rate)
        self.iter = iteration

        self.scanned = False

    def run(self):
        try:
            self.lib.scan(self.P, self.c_rate, self.c_dur)
            self.scanned = True
            print("Scanner ", self.iter, " has completed scan.")
        except Exception:
            print('Scan error')
            sys.exit(1)


class Writer(threading.Thread):
    def __init__(self, scan_thread, iter):
        threading.Thread.__init__(self)
        self.iter = str(iter)
        self.to_write = []
        self.scan_thread = scan_thread

    def run(self):
        while True:
            if self.scan_thread.scanned:
                self.to_write = np.fromiter(
                    self.scan_thread.P, dtype=np.int, count=self.scan_thread.len)
                self.scan_thread.lib.release(self.scan_thread.P)
                pickle.dump(self.to_write, open(
                    "Output/output" + self.iter + ".bin", "wb"))
                print("Writer  ", self.iter, " has completed write.")
                break


if __name__ == '__main__':
    COUNT = 10

    threads = []
    lib = CDLL("src/scan.dll")
    pathlib.Path('Output').mkdir(parents=True, exist_ok=True)
    for i in range(COUNT):
        threads.append(Scanner(i, lib))
        threads[-1].start()
        threads.append(Writer(threads[-1], i).start())

        scan_threads = threads[::2]
        for thread in scan_threads:
            thread.join()
