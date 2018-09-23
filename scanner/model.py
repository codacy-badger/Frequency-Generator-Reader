"""
 **File Name:** model.py                                                                         \n
 **Project:** CURRENTLY UNNAMED                                                                  \n
 **Company:** Research in Flows, Inc                                                             \n
 **Author:** David A. Gurevich                                                                   \n

Frequency-Generator Reader | Local software for generating and processing high-frequency signals
Copyright (C) 2018  David A. Gurevich
"""

from wtforms import Form, FloatField, BooleanField, validators


class InputForm(Form):
    fq = FloatField(
        label='Frequency (Hz)', default=1000.0,
        validators=[validators.DataRequired(), validators.NumberRange(1, 35000000)])
    amp = FloatField(
        label='Amplitude (V)', default=1.0,
        validators=[validators.InputRequired(), validators.NumberRange(0, 1)])
    rate = FloatField(
        label='Scan Rate (Hz)', default=16000000.0,
        validators=[validators.InputRequired(), validators.NumberRange(1000, 20000000)])
    dur = FloatField(
        label='Duration (s)', default=0.001,
        validators=[validators.InputRequired(), validators.NumberRange(0, 2)])
    thread_count = FloatField(
        label='Thead Count', default=3,
        validators=[validators.InputRequired()])
    graph_data = BooleanField(
        label='Graph Data?', default=True)
