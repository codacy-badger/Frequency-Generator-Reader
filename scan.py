"""
 **File Name:** scan.py                                                                                               \n
 **Project:** CURRENTLY UNNAMED                                                                                       \n
 **Company:** Research in Flows, Inc                                                                                  \n
 **Author:** David Gurevich                                                                                           \n
 **Required Modules:**
       * numpy                                                                                                        \n

This work is licensed under the Creative Commons Attribution-NonCommercial-NoDerivs 3.0 Unported License.
To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-nd/3.0/ or send a letter to
Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
"""

import csv
import os
import pathlib
import sys

import numpy as np

from hantekdds import htdds_wrapper as hantek
from src import plot
from src.input_func import get_input, SCAN_OPTIONS

if __name__ == '__main__':

    function_generator = hantek.HantekDDS()
    if not function_generator.connect():
        print("Failed to connect to Hantek 1025G module.")
        sys.exit()

    bool_gen_fq, fq, voltage, dur, scan_fq, scan_option, bool_graph = get_input()

    if bool_gen_fq:
        function_generator.drive_periodic(voltage, fq)

    pathlib.Path('Output').mkdir(parents=True, exist_ok=True)

    config_file = open('Output/config.txt', 'w')
    config_file.write(
        str(scan_fq * dur) + "\n" +
        str(scan_fq) + "\n" +
        str(int(SCAN_OPTIONS[scan_option.upper()]))
    )
    config_file.close()

    os.system("C_ScanA.exe")

    # Get DAQ data

    eng_unit_signal = []

    with open('Output/daq_output.csv') as daq_out:
        next(daq_out, None)
        rows = csv.reader(daq_out)
        for row in rows:
            eng_unit_signal.append(float(row[1]))
    # Write fourier transformation

    fourier_transform = np.fft.rfft(eng_unit_signal)

    with open('Output/fourier_output.csv', 'w') as fourier_output_file:
        out_writer = csv.writer(fourier_output_file)
        out_writer.writerows(map(lambda x: [x], fourier_transform))

    if bool_graph:
        plot.graph_input(eng_unit_signal, scan_fq, fourier_transform, dur)
    sys.exit()
