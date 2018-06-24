# bintocsv.py
# Written by David Gurevich
#
# Intended to convert pickled .bin files to .csv files
# for downstream and upstream scanners

import pickle
import csv
import sys

def binToCSV(binFile):
    int_data =  []
    int_chan1 = []
    int_chan2 = []

    with open(binFile, 'rb') as fp:
        int_data = pickle.load(fp)

    int_chan1 = int_data[::2]
    int_chan2 = int_data[1::2]

    new_file_name = binFile[:len(binFile) - 3] + "csv"

    with open(new_file_name, 'w') as csvFile:
        csv_writer = csv.writer(csvFile)
        for i in range(len(int_chan1)):
            csv_writer.writerow([int(int_chan1[i]), int(int_chan2[i])])

if __name__ == '__main__':
    for x in range(len(sys.argv) - 1):
        binToCSV(sys.argv[x + 1])
