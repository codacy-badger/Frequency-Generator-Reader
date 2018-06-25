# Frequency Generator and Reader

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/a7f6ffc1e54c4987857f00c48a3705c7)](https://app.codacy.com/app/davidgur/Frequency-Generator-Reader?utm_source=github.com&utm_medium=referral&utm_content=davidgur/Frequency-Generator-Reader&utm_campaign=badger)

The currently unnamed frequency generator and reader, which, upon completion will be used in ultrasonic utilities in industrial applications.

It is controlled by a Flask-run control panel that can be started by running ```controller.py```.
It interacts with the Hantek 1025G 25MHz Arbitrary function generator as well as the Measurement Computing USB 2020 high-speed simultaneous USB DAQ device.

This project was built using [Atom](http://atom.io).

## Running the Software

**Prerequisites:**
* Windows - Due to the lack of drivers, this software only works in Windows.
* Hantek 1025G Drivers - You will have to get the Windows drivers for the generator. You will probably run into problems installing these drivers because they were poorly made and I hate them.
* Measurement Computing InstaCal - This is the configuration software for the Measurement Computing USB2020.
* The Following Python Libraries:
  * MatPlotLib (Plotting)
  * NumPy      (NumPy Arrays)
  * MCCULW     (Measurement Computing SDK)
  * Flask      (This project uses flask)
  * WTForms    (Form building)

**Actually running the software:**

Simply execute ```scan.py``` in the ```scanner``` folder for a basic scan, or execute ```controller.py``` for a full control panel.

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
