"""
 **File Name:** bin_to_csv.py                                                                    \n
 **Project:** CURRENTLY UNNAMED                                                                  \n
 **Company:** Research in Flows, Inc                                                             \n
 **Author:** David A. Gurevich                                                                   \n

Frequency-Generator Reader | Local software for generating and processing high-frequency signals
Copyright (C) 2018  David A. Gurevich
"""

import csv
import os
import pickle
import shutil


def zip_folder(folder_path, output_path):
    """
    Makes a ZIP folder out of a regular Windows directory.
    """
    shutil.make_archive(output_path, 'zip', folder_path)


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


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

    for i, filename in enumerate(os.listdir('Output')):
        file_path = 'Output/' + filename
        with open('Output/' + filename, 'rb') as fp:
            int_data = pickle.load(fp)
        int_chan1 = int_data[::2]
        int_chan2 = int_data[1::2]

        new_file_name = file_path[:len(file_path) - 4]

        split_int_chan1 = list(chunks(int_chan1, int(1E6)))
        split_int_chan2 = list(chunks(int_chan2, int(1E6)))

        paired_list = [[split_int_chan1[x], split_int_chan2[x]] for x in range(len(split_int_chan1))]

        for x, pair in enumerate(paired_list):
            with open(new_file_name + "-" + str(x + 1) + ".csv", 'w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                for j, val in enumerate(pair[0]):
                    csv_writer.writerow([val, pair[1][j]])

        os.unlink(file_path)
    try:
        os.unlink('static/output.zip')
    except FileNotFoundError:
        print("No existing output.zip")
    zip_file_name = 'static/output'
    zip_folder('Output', zip_file_name)

    return zip_file_name
