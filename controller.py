"""
 **File Name:** controller.py                                                                    \n
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

import sys

from model import InputForm
from flask import Flask, render_template, request

from scanner.scan import run_scan
from scanner.bin_to_csv import bin_to_csv
from scanner.gen_png import gen_image

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def csv_index():
    form = InputForm(request.form)
    if request.method == 'POST' and form.validate():
        if run_scan(form.fq.data, form.rate.data, form.dur.data, form.thread_count.data):
            if form.graph_data.data:
                png_img = gen_image()
            else:
                png_img = None
            zip_file = bin_to_csv()
    else:
        png_img = None
        zip_file = None

    return render_template('index.html', form=form, result=zip_file, img=png_img)


if __name__ == '__main__':
    app.run(debug=True)
