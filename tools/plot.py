"""
Bokeh plotter for Research in Flows, Inc Scan utility

Copyright (c) David Gurevich 2018
"""

import csv
import os

from bokeh.embed import components
from bokeh.plotting import figure


def create_figure():
    """
    Reads all files in Output folder, plots them, and returns
    the HTML and JavaScript Code to plot the signal online as a tuple.

    Returns:
        script, div (tuple): The components of the plot (p) that
                            are used to graph the signal in the browser.
    """
    chan1 = []
    chan2 = []

    for file in os.listdir("Output"):
        with open("Output/" + file) as fp:
            csv_reader = csv.reader(fp, delimiter=',')
            for row in csv_reader:
                chan1.append(float(row[0]))
                chan2.append(float(row[1]))

    p = figure(sizing_mode='scale_width', height=380, output_backend='webgl', toolbar_location='below')

    p.line(range(len(chan1)), chan1, legend="Channel 1", line_width=2, line_color="aqua")
    p.line(range(len(chan2)), chan2, legend="Channel 2", line_width=2, line_color="orange")

    script, div = components(p)

    del chan1
    del chan2

    return script, div
