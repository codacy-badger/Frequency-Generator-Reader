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
    chan1 = []
    chan2 = []

    for file in os.listdir("Output"):
        with open("Output/" + file) as fp:
            csv_reader = csv.reader(fp, delimiter=',')
            for row in csv_reader:
                chan1.append(float(row[0]))
                chan2.append(float(row[1]))

    # Plotting happens here

    p = figure(sizing_mode='scale_width', height=380, output_backend="webgl", toolbar_location="below")

    p.line(range(len(chan1)), chan1, legend="Channel 1", line_width=2, line_color="aqua")
    p.line(range(len(chan2)), chan2, legend="Channel 2", line_width=2, line_color="orange")

    script, div = components(p)

    return script, div
