"""
Utility function for Research in Flows, Inc Scan utility

Copyright (c) David Gurevich 2018
"""

import os
import shutil


def zip_folder():
    """
    Makes a ZIP folder out of a regular Windows directory.
    """
    try:
        os.unlink('static/Output.zip')
    except FileNotFoundError:
        print("No existing ZIP folder.")

    shutil.make_archive("static/Output", "zip", "Output/")
    return "static/Output"
