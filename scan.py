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
