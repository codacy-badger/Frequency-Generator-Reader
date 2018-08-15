#!/usr/bin/python
"""
 **File Name:** controller.py                                                                    \n
 **Project:** CURRENTLY UNNAMED                                                                  \n
 **Company:** Research in Flows, Inc                                                             \n
 **Author:** David A. Gurevich                                                                   \n

Frequency-Generator Reader | Local software for generating and processing high-frequency signals
Copyright (C) 2018  David A. Gurevich
"""

import os
import sys

from flask import Flask, render_template, request

from scanner.IPDetector import get_local_ip
from scanner.model import InputForm
from scanner.plot import create_figure
from scanner.scan import run_scan
from scanner.write_csv import zip_folder

if getattr(sys, 'frozen', False):
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    static_folder = os.path.join(sys.executable, '..', 'static')
    app = Flask(__name__, template_folder=template_folder)
else:
    app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Page to be loaded when user connects to host:5000/

    Attr:
        form: Class from model.py -- Contains input forms for scan information.
        zip_file: Zip file generated by bin_to_csv.py containing data files.
        png_img: base64 encoded PNG image of graphed data.
    """
    form = InputForm(request.form)
    plots = []
    zip_file = None
    try:
        if request.method == 'POST' and form.validate():
            scan_status, crit_time_list = run_scan(form.fq.data, form.amp.data, form.rate.data, form.dur.data,
                                                   form.thread_count.data)
            crit_time_list = [str((float(x) - float(crit_time_list[0])) / 1E9) for x in crit_time_list]

            start_times = []
            end_times = []

            for i in range(0, len(crit_time_list), 2):
                start_time = crit_time_list[i]
                end_time = crit_time_list[i + 1]
                start_times.append(start_time)
                end_times.append(end_time)

            if scan_status:
                zip_file = zip_folder()
                if form.graph_data.data:
                    plots.append(create_figure())
            else:
                error_page("There was a problem scanning. Consult Console.")
        else:
            zip_file = None
    except Exception as e:
        print(e)
        error_page(str(e))
    return render_template('index.html', form=form, result=zip_file, plots=plots)


@app.route('/errortest')
def error_page(exception_message="This is a test error page."):
    return render_template('500.html', exception_message=exception_message)


if __name__ == '__main__':
    app.run(debug=True, host=get_local_ip(), port=80)
