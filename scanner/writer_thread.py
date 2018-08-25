"""
 **File Name:** writer_thread.py                                                                 \n
 **Project:** CURRENTLY UNNAMED                                                                  \n
 **Company:** Research in Flows, Inc                                                             \n
 **Author:** David A. Gurevich                                                                   \n

Frequency-Generator Reader | Local software for generating and processing high-frequency signals
Copyright (C) 2018  David A. Gurevich
"""

import threading

from scanner.write_csv import write_csv


class Writer(threading.Thread):
    """
    Thread responsible for writing information retrieved by scanner thread.

    Checks if scanner thread is finished scanning.
    If it is, convert the information (from pointer) into an iterable that Python
    understands. Then, pickle and dump the information. Finally, release the pointer.

    Attributes:
        thread_id (int):                    iter argument saved to respective thread.
        to_write (list):               Iterable that the pointer will be converted into.
        scan_thread (Scanner() Class): scan_thread argument saved to respective thread.
    """

    def __init__(self, scan_thread, thread_id, dll_lib):
        """
        Initialization of Writer thread.

        Args:
            scan_thread (Scanner() Class):The writer's corresponding scan thread that it reports to.
            thread_id (int):                    Iteration of for loop that generates the thread.
        """
        threading.Thread.__init__(self)

        self.thread_id = str(thread_id + 1)
        self.to_write = []
        self.scan_thread = scan_thread
        self.dll_lib = dll_lib
        self.complete = False

    def run(self):
        """
        Write information retrieved from Scanner thread.

        Checks if scanner thread has completed scan. If it has,
        Tries to convert pointer to list. Then, pickles and dumps
        the list. Finally, releases the pointer.
        """
        while True:
            if self.scan_thread.complete:  # Check if scanner thread is complete
                write_csv(self.scan_thread.p, self.scan_thread.len // 2, self.thread_id)
                self.scan_thread.lib.release(self.scan_thread.p)  # Release the thread when done
                self.complete = True
                break

        return
