"""
 **File Name:** bin_to_csv.py                                                                    \n
 **Project:** CURRENTLY UNNAMED                                                                  \n
 **Company:** Research in Flows, Inc                                                             \n
 **Author:** David A. Gurevich                                                                   \n

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
import shutil
import csv
import sys
import os


def zip_folder(folder_path, output_path):
    shutil.make_archive(output_path, 'zip', folder_path)


def bin_to_csv():
    int_data = []
    int_chan1 = []
    int_chan2 = []

    for filename in os.listdir('Output'):
        file_path = 'Output/' + filename
        with open('Output/' + filename, 'rb') as fp:
            int_data = pickle.load(fp)

        int_chan1 = int_data[::2]
        int_chan2 = int_data[1::2]

        new_file_name = file_path[:len(file_path) - 3] + "csv"

        with open(new_file_name, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            for i in range(len(int_chan1)):
                csv_writer.writerow([int_chan1[i], int_chan2[i]])

        os.unlink(file_path)

    zip_file_name = 'static/output'
    zip_folder('Output', zip_file_name)
    return zip_file_name


if __name__ == '__main__':
    bin_to_csv()
