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
import os


def zip_folder(folder_path, output_path):
    """
    Makes a ZIP folder out of a regular Windows directory.
    """
    shutil.make_archive(output_path, 'zip', folder_path)


def bin_to_csv():
    """
    Converts dumped .bin files into human-readable CSV files.

    Attr:
        int_data: List of collected data in integer form.
        int_chan1: List of collected data from channel 1 in integer form.
        int_chan2: List of collected data from channel 2 in integer form.
        new_file_name: The name of the CSV file to be saved.
        zip_file_name: The name of the ZIP folder where all the CSV files should be placed.
    """
    int_data =  []  # All Data
    int_chan1 = []  # Channel 0
    int_chan2 = []  # Channel 1

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
    try:
        os.unlink('static/output.zip')
    except:
        print("No existing output.zip")
    zip_file_name = 'static/output'
    zip_folder('Output', zip_file_name)
    return zip_file_name


if __name__ == '__main__':
    bin_to_csv()
