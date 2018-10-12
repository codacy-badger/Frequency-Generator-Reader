"""
InputForm for Research in Flows, Inc Scan Utility

Copyright (c) David Gurevich 2018
"""

from wtforms import Form, FloatField, BooleanField, validators


class InputForm(Form):
    """
    Generates fields for the form and their validators.
    Most fields require data and for that data to be in a certain range.
    """
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
        label='Thread Count', default=3,
        validators=[validators.InputRequired()])
    graph_data = BooleanField(
        label='Graph Data?', default=True)
