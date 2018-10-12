"""
Utility function for Research in Flows, Inc Scan utility

Copyright (c) David Gurevich 2018
"""


def empty_output_folder():
    """
    Ensures that there is an Output folder and that
    it is empty.
    """
    import os
    if not os.path.exists("Output"):
        os.makedirs("Output")

    folder = 'Output'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)
