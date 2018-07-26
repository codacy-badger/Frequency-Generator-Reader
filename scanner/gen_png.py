"""
 **File Name:** gen_png.py                                                                       \n
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
import os
import io
import base64
import csv

from matplotlib import pyplot as plt
from matplotlib.lines import Line2D


def gen_image():
    """
    (None) --> Base64 Encoded PNG Image

    Scans the output files of scan.py, plots the data
    using matplotlib, and exporting it as a PNG base64 encoded image.

    Attr:
        data: List containing all collected data.
        chan1: Every odd element in 'data' list. Represents 1st channel collection.
        chan2: Every even element in 'data' list. Represents 2nd channel collection.
        plot_url: MatPlotLib graph exported as a png and encoded in base64.
        file_count: Number of files in 'Output' folder.

    """
    timestamp = []
    chan1 = []
    chan2 = []

    path, dirs, files = next(os.walk("Output"))
    file_count = len(files)
    for i in range(file_count):
        str_i = str(i)
        with open('Output/output' + str_i + '.csv') as fp:
            csv_reader = csv.reader(fp, delimiter=',')
            for row in csv_reader:
                timestamp.append(float(row[0]))
                chan1.append(float(row[1]))
                chan2.append(float(row[2]))

    img = io.BytesIO()

    plt.rcParams["figure.figsize"] = (16, 9)

    plt.plot(timestamp, chan1, "o", label="Channel 1")
    plt.plot(timestamp, chan2, "o", label="Channel 2")

    legend_elements = [Line2D([0], [0], color='b', lw=4, label="Channel 1"),
                       Line2D([0], [0], color='orange', lw=4, label="Channel 2")]

    legend = plt.legend(handles=legend_elements, loc='lower right')

    plt.title("Amplitude (V) vs Time (nS)")
    plt.ylabel("Amplitude (12-bit digital value)")
    plt.xlabel("Time (nS)")

    plt.savefig(img, format="png")
    plt.clf()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    return plot_url


if __name__ == '__main__':
    gen_image()
