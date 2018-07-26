"""
 **File Name:** model.py                                                                         \n
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

from wtforms import Form, FloatField, BooleanField, validators


class InputForm(Form):
    fq = FloatField(
        label='Frequency (Hz)', default=1000000.0,
        validators=[validators.InputRequired()])
    amp = FloatField(
        label='Amplitude (V)', default=1.0,
        validators=[validators.InputRequired()])
    rate = FloatField(
        label='Scan Rate (Hz)', default=16000000.0,
        validators=[validators.InputRequired()])
    dur = FloatField(
        label='Duration (s)', default=0.001,
        validators=[validators.InputRequired()])
    thread_count = FloatField(
        label='Thead Count', default=3,
        validators=[validators.InputRequired()])
    graph_data = BooleanField(
        label='Graph Data?', default=True)
