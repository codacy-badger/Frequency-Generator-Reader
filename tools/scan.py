"""
Scan module for Research in Flows, Inc Scan Utility

Uses function (runDAQScanDLL()) found in ScanUtilLib/ScanUtils.dll
to run a scan with user-provided arguments and write the results to
multiple files.

runDAQScanDLL is multi-threaded.

Copyright (c) David Gurevich 2018
"""

from tools.hantekdds.htdds_wrapper import HantekDDS


def function_generator_connected():
    """
    function_generator_connected() --> bool

    Returns:
        True if program was able to connect to Hantek 1025G Hardware.
        False if program was unable to connected to Hantek 1025G Hardware.
    """
    function_generator = HantekDDS()
    if not function_generator.connect():
        return False
    else:
        return True


def daq_connected():
    """
    daq_connected() --> bool

    Gets a test value from the USB2020. If there is an error during the process, then the
    USB2020 is unavailable for use.

    Returns:
        True if no errors occurred during test data acquisition.
        False if errors occurred during test data acquisition.
    """
    from mcculw import ul
    from mcculw.enums import ULRange
    from mcculw.ul import ULError

    board_num = 0
    channel = 0
    ai_range = ULRange.BIP5VOLTS

    try:
        ul.a_in(board_num, channel, ai_range)
        return True
    except ULError:
        return False


def run_scan(scan_parameters, function_generator_parameters):
    """
    Sets up the user-specified scan by loading the
    library where the function is provided, and determining
    whether the hardware is connected.

    If the conditions for the scan are such that the scan
    can be conducted, then the scan is executed.

    Args:
        scan_parameters (tuple): Tuple containing the num_of_threads, scan_rate,
                                and scan_duration as specified in the controller
                                (controller.py)
        function_generator_parameters (tuple): Tuple containing the frequency
                                            and amplitude of function to be
                                            generated.

    Returns:
        errors (list): List of errors that have occurred during the scan.

    """
    from ctypes import cdll, c_double, c_int

    errors = []

    ScanUtils = cdll.LoadLibrary("ScanUtilLib/ScanUtils.dll")
    frequency, amplitude = function_generator_parameters
    num_of_threads, scan_rate, scan_duration = scan_parameters

    function_generator = HantekDDS()
    if function_generator_connected():
        function_generator.drive_periodic(frequency=float(frequency), amplitude=float(amplitude))
    else:
        print("FATAL ERROR: Could not connect to Hantek 1025G Module.")
        errors.append("Hantek 1025G not connected")

    if daq_connected:
        try:
            ScanUtils.runDAQScanDLL(c_int(num_of_threads), c_int(scan_rate), c_double(scan_duration))
        except Exception as e:
            print("FATAL ERROR: ", e)
            errors.append(str(e))

    else:
        print("FATAL ERROR: Could not connect to Measurement Computing USB2020 module.")
        errors.append("USB2020 not connected")

    return errors
