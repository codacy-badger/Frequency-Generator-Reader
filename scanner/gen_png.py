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

from matplotlib import pyplot as plt


def gen_image():
    data = []
    path, dirs, files = next(os.walk("Output"))
    file_count = len(files)
    for i in range(file_count):
        str_i = str(i)
        with open('Output/output' + str_i + '.bin', 'rb') as fp:
            to_add = pickle.load(fp)
            data.extend(to_add)

    chan1 = data[::2]
    chan2 = data[1::2]

    img = io.BytesIO()
    plt.rcParams["figure.figsize"] = (16, 9)
    plt.plot(chan1)
    plt.plot(chan2)
    plt.savefig(img, format="png")
    plt.clf()
    img.seek(0)

    plot_url = base64.b64encode(img.getvalue()).decode()
    return plot_url


if __name__ == '__main__':
    gen_image()
