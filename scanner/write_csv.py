"""
 **File Name:** write_csv.py                                                                    \n
 **Project:** CURRENTLY UNNAMED                                                                  \n
 **Company:** Research in Flows, Inc                                                             \n
 **Author:** David A. Gurevich                                                                   \n

Frequency-Generator Reader | Local software for generating and processing high-frequency signals
Copyright (C) 2018  David A. Gurevich
"""
import os
import shutil

import numpy as np


def zip_folder():
    """
    Makes a ZIP folder out of a regular Windows directory.
    """
    try:
        os.unlink('static/Output.zip')
    except FileNotFoundError:
        print("No existing ZIP folder.")

    shutil.make_archive("static/Output", "zip", "Output/")
    return "static/Output"


def chunks(l, n):
    """
    Yield successive n-sized chunks from l.
    """
    for i in range(0, len(l), n):
        yield l[i:i + n]


def write_csv(c_types_array, length, thread_id):
    try:
        data = np.fromiter(c_types_array, dtype=np.int, count=int(length * 2))
        chan_1 = data[::2]
        chan_2 = data[1::2]
    except ValueError:
        return False

    split_chan1 = list(chunks(chan_1, int(1E6)))
    split_chan2 = list(chunks(chan_2, int(1E6)))

    paired_list = [[split_chan1[x], split_chan2[x]] for x in range(len(split_chan1))]

    for x, pair in enumerate(paired_list):
        file_name = "Output/DAQ_Output_" + thread_id + "_" + str(x + 1) + ".csv"
        np.savetxt(file_name, np.c_[pair[0], pair[1]], delimiter=',', fmt='%i')

    del paired_list
