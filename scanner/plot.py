"""
 **File Name:** plot.py                                                                          \n
 **Project:** CURRENTLY UNNAMED                                                                  \n
 **Company:** Research in Flows, Inc                                                             \n
 **Author:** David A. Gurevich                                                                   \n

Frequency-Generator Reader | Local software for generating and processing high-frequency signals
Copyright (C) 2018  David A. Gurevich
"""

import csv
import os

from bokeh.embed import components
from bokeh.plotting import figure


def create_figure():
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

    # Plotting happens here

    p = figure(sizing_mode='scale_width', height=380, output_backend="webgl", toolbar_location="below")

    p.line(timestamp, chan1, legend="Channel 1", line_width=2, line_color="aqua")
    p.line(timestamp, chan2, legend="Channel 2", line_width=2, line_color="orange")

    script, div = components(p)

    return script, div
