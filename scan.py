#!/usr/bin/env python

"""
 **File Name:** scan.py                                                       \n
 **Project** CURRENTLY UNNAMED                                                \n
 **Company:** Research in Flows, Inc                                          \n
 **Author:** David Gurevich                                                   \n
 **Required Modules:**
       * input_func.py                                                        \n
       * hantekdds/htdds_wrapper.py                                           \n

This work is licensed under the Creative Commons
Attribution-NonCommercial-NoDerivs 3.0 Unported License.
To view a copy of this license, visit
http://creativecommons.org/licenses/by-nc-nd/3.0/ or send a letter to
Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
"""

import os
import sys
import pathlib
import csv
import shutil

from input_func import get_input, SCAN_OPTIONS
from hantekdds import htdds_wrapper as hantek
import demodulate
import plot

if __name__ == '__main__':
    FUNCTION_GENERATOR = hantek.HantekDDS()
    if not FUNCTION_GENERATOR.connect():
        print("Failed to Connect to HantekDDS.")
        sys.exit()

    shutil.rmtree('Output', ignore_errors=True)

    GEN_FQ_BOOL, FREQUENCY, VOLTAGE, SECONDS, SCAN_RATE, SCAN_OPTION, GRAPH_OPTION, USE_MATLAB_BOOL, FILTER_SENSITIVITY = get_input()
    COUNT = SCAN_RATE * SECONDS
    if GEN_FQ_BOOL:
        FUNCTION_GENERATOR.drive_periodic(VOLTAGE, FREQUENCY)

    pathlib.Path('Output').mkdir(parents=True, exist_ok=True)
    FILE = open('Output/config.txt', 'w')
    FILE.write(str(COUNT) + "\n" + str(SCAN_RATE) +
               "\n" + str(int(SCAN_OPTIONS[SCAN_OPTION])))
    FILE.close()

    os.system("C_ScanA.exe")

    TO_GRAPH = []

    with open('Output/daq_output.csv') as f:
        next(f, None)
        rows = csv.reader(f)
        for row in rows:
            TO_GRAPH.append(float(row[1]))

    analytic_signal, amplitude_envelope, fil_amplitude_envelope = demodulate.hilbert_envelope(
        SECONDS, SCAN_RATE, TO_GRAPH, FILTER_SENSITIVITY)

    with open('Output/output.csv', 'w') as n_f:
        with open('Output/daq_output.csv', 'r') as o_f:
            n_writer = csv.writer(n_f)
            n_writer.writerow(
                ['RAW VALUE', 'VOLTAGE', 'ENVELOPE', 'FILTERED ENVELOPE'])
            next(o_f, None)
            o_rows = csv.reader(o_f)
            for i, row in enumerate(o_rows):
                row.extend([amplitude_envelope[i], fil_amplitude_envelope[i]])
                n_writer.writerow(row)

    os.remove('Output/daq_output.csv')

    if GRAPH_OPTION and not USE_MATLAB_BOOL:
        plot.show_data(analytic_signal, amplitude_envelope, fil_amplitude_envelope)
    elif GRAPH_OPTION and USE_MATLAB_BOOL:
        os.system("matlab_plot.exe")

    sys.exit()
