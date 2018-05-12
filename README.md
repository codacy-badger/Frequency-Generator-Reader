# Frequency Generator and Reader

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/a7f6ffc1e54c4987857f00c48a3705c7)](https://app.codacy.com/app/davidgur/Frequency-Generator-Reader?utm_source=github.com&utm_medium=referral&utm_content=davidgur/Frequency-Generator-Reader&utm_campaign=badger)

The currently unnamed frequency generator and reader, which, upon completion will be used in ultrasonic utilities in industrial applications.

It interacts with the Hantek 1025G 25MHz Arbitrary function generator as well as the Measurement Computing USB 2020 high-speed simultaneous USB DAQ device.

This project allows the user to control the devices through a command line interface. The user can enter initial settings, and then run a scan. The ***input frequency***, ***input voltage***, ***duration***, ***scan rate***, and ***scan mode*** are all user controlled.

This project was built using [Atom](http://atom.io).

## Algorithms and Process
As of right now, the software assumes an amplitude-modulated wave as input, and using the fourier transformation, determines the frequency of the encoded wave. There is some innacuracy to it, notably, sometimes the detected frequency is a multiple of the actual frequency. This is all very work in progress. 

![alt text](https://wikimedia.org/api/rest_v1/media/math/render/svg/97ad0938a279c4846d42a4bbd212f6a1f0ca4c0f "Fourier Transformation")

Frequency-modulation and phase-modulation detection is currently in the works.

## Output

The output consists of 3 files and 1 window.
* ```config.txt``` - This file is used by the C software to determine how to scan the wave
* ```daq_output.csv``` - This file contains both the raw values and the voltage values from the scanning application
* ```fourier_output.csv``` - This file contains the fourier transformation of the voltage-based signal from the DAQ
* ```output.csv``` - All-in-one output file containing information about the graph such as the values, fft, and envelope
* ```OutputPlot.png``` - This is a PyPlot that graphs the elements in ```daq_output.csv``` and ```fourier_output.csv```
* PyPlot window that graphs all elements in ```daq_output.csv``` and ```fourier_output.csv```

## Running the Software

**Prerequisites:**
* Windows - Due to the lack of drivers, this software only works in Windows.
* Hantek 1025G Drivers - You will have to get the Windows drivers for the generator. You will probably run into problems installing these drivers because they were poorly made and I hate them.
* Measurement Computing InstaCal - This is the configuration software for the Measurement Computing USB2020.
* The Following Python Libraries:
  * MatPlotLib (Plotting)
  * NumPy      (NumPy Arrays and FFT)
  * PeakUtils  (Determine Peaks in FFT)
  * MCCULW     (Measurement Computing SDK)

**Actually running the software:**

Simply execute ```scan.py```



## Authors

* [**David Gurevich**](https://github.com/davidgur) - *All work so far*

## License

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
