"""
 **File Name:** scanner_thread.py                                                                \n
 **Project:** CURRENTLY UNNAMED                                                                  \n
 **Company:** Research in Flows, Inc                                                             \n
 **Author:** David A. Gurevich                                                                   \n

Frequency-Generator Reader | Local software for generating and processing high-frequency signals
Copyright (C) 2018  David A. Gurevich
"""

import threading
from ctypes import c_int, c_longlong, c_double, POINTER, byref


class Scanner(threading.Thread):
    """
    Thread responsible for retrieving information from USB-2020 Module.

    This class if a child class of the threading.Thread class. It is to be
    executed as a thread ( thread.start() .)

    Attributes:
        lib (ctypes.CDLL):           CTypes DLL file to use for scanning functions.
        lib.scan.argtypes (list):    Arguments that the scan function takes (from DLL.)
        lib.scan.restype  (list):    Return values of scan function (from DLL.)
        lib.release.argtypes (list): Arguments that the release function takes (from DLL.)
        lib.release.restype (list):  Return values of release function (from DLL.)
        rate (int):                  Scan rate.
        c_rate (c_int):              CTypes c_int version of rate.
        dur (float):                 Duration of scan in seconds.
        c_dur (c_double):            CTypes c_double version of dur.
        p (POINTER(c_int)):          List "retrieval" from scan function.
        len (int):                   Number of points to scan.
        iter (int):                  Number generated in for loop when designating threads.
    """

    def __init__(self, iteration, dll_lib, rate, dur, time_collector):
        """
        Initialization of Scanner thread.

        Args:
            iteration (int):       for loop iteration when generating thread. For identification purposes.
            dll_lib (ctypes.CDLL): CTypes DLL file to be used for scanning functions.

        """
        threading.Thread.__init__(self)
        self.lib = dll_lib

        # void scan(int** input, int rate, double dur) {}
        self.lib.scan.argtypes = [POINTER(POINTER(c_int)), POINTER(c_longlong), POINTER(c_longlong), c_int, c_double]
        self.lib.scan.restype = None

        # void release(int* input) {}
        self.lib.release.argtypes = [POINTER(c_int)]
        self.lib.release.restype = None

        self.rate = int(rate)  # Convert rate (float) to integer
        self.c_rate = c_int(self.rate)  # convert self.rate to C integer

        self.dur = dur
        self.c_dur = c_double(self.dur)  # Convert duration to C double

        self.p = POINTER(c_int)()  # Generate integer pointer
        self.len = int(2 * self.rate * self.dur)
        self.iter = iteration  # Thread identifier

        self.start_time = c_longlong(0)
        self.end_time = c_longlong(0)

        self.time_collector = time_collector

        self.complete = False  # Completion signal to check when data can be written

    def run(self):
        """
        Scan and retrieve information from USB 2020 module.

        Tries to scan to an integer pointer at a predetermined rate and duration.
        When scanned, set scanned to True in order to indicate to WRITER thread
        that it can start writing.
        """
        self.lib.scan(self.p, byref(self.start_time), byref(self.end_time), self.c_rate, self.c_dur)

        self.time_collector.put((self.start_time.value, self.end_time.value))
        self.complete = True

        return
