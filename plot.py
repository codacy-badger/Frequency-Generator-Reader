"""
 **File Name:** plot.py                                                                                               \n
 **Project:** CURRENTLY UNNAMED                                                                                       \n
 **Company:** Research in Flows, Inc                                                                                  \n
 **Author:** David Gurevich                                                                                           \n
 **Required Modules:**
       * numpy                                                                                                        \n
       * matplotlib.pyplot                                                                                            \n

This work is licensed under the Creative Commons Attribution-NonCommercial-NoDerivs 3.0 Unported License.
To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-nd/3.0/ or send a letter to
Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
"""

import matplotlib.pyplot as plt
import numpy as np

np.warnings.filterwarnings('ignore')


def show_data(analytic_signal, amplitude_envelope, fil_amplitude_envelope):
    x = np.arange(len(analytic_signal))

    y = analytic_signal
    plt.plot(x, y, label='Received Signal')

    y = amplitude_envelope
    plt.plot(x, y, label='Hilbert Transformation')

    y = fil_amplitude_envelope
    plt.plot(x, y, label='Filtered Envelope')

    plt.xlabel('Point number')
    plt.ylabel('Voltage (V)')
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
               ncol=2, mode="expand", borderaxespad=0.)

    plt.savefig('Output/OutputPlot.png')
    plt.show()
