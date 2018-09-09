#!/usr/bin/python
"""
 **File Name:** string_tool.py                                                                   \n
 **Project:** CURRENTLY UNNAMED                                                                  \n
 **Company:** Research in Flows, Inc                                                             \n
 **Author:** David A. Gurevich                                                                   \n

Frequency-Generator Reader | Local software for generating and processing high-frequency signals
Copyright (C) 2018  David A. Gurevich
"""


def to_hz(val):
    """
    Converts float or integer to a human-readable value with the appropriate Hertz suffix.
    Args:
        val: Value to be converted into string with units.

    Returns:
        String with val and respective Hertz suffix.
    """
    if val < 1000:
        return str(val) + " Hz"
    elif 1000 <= val < int(1e6):
        return str(val / 1000) + " KHz"
    elif int(1e6) <= val:
        return str(val / int(1e6)) + " MHz"
    else:
        return str(val)


def to_volts(val):
    """
    Converts float or integer to a human-readable value with the appropriate Volts suffix.
    Args:
        val: Value to be converted into string with units.

    Returns:
        String with val and respective Volts suffix.
    """
    if val < 1:
        return str(val / 1000) + " mV"
    elif 1 <= val < 1000:
        return str(val) + " V"
    elif 1000 < val < int(1e6):
        return str(val) + " KV"
    elif int(1e6) <= val:
        return str(val) + " MV"
    else:
        return str(val)
