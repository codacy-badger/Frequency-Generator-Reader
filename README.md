# Frequency Generator and Reader
 The currently unnamed frequency generator and reader, which, upon completion will be used in ultrasonic utilities in industrial applications.
 It is controlled by a Flask-run control panel that can be started by running ```controller.py```.
It interacts with the Hantek 1025G 25MHz Arbitrary function generator as well as the Measurement Computing USB 2020 high-speed simultaneous USB DAQ device.
 ## Running the Software
 **Prerequisites:**
* Windows - Due to the lack of drivers, this software only works in Windows.
* Hantek 1025G Drivers - You will have to get the Windows drivers for the generator. You will probably run into problems installing these drivers because they were poorly made and I hate them.
* Measurement Computing InstaCal - This is the configuration software for the Measurement Computing USB2020.
* The Following Python Libraries:
  * MCCULW     (Measurement Computing SDK)
  * Flask      (This project uses flask)
  * WTForms    (Form building)
 ## Authors
 * [**David Gurevich**](https://github.com/davidgur) - *All work so far*
 ## License
 Frequency-Generator Reader | Local software for generating and processing high-frequency signals
Copyright (C) 2018  David A. Gurevich
