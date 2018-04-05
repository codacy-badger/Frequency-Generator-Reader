# Frequency Generator and Reader

The currently unnamed frequency generator and reader, which, upon competion will be used in CrossFlow utilities in industrial applications.

It interacts with the Hantek 1025G 25MHz Arbitrary function generator as well as the Measurement Computing USB 2020 high-speed simultaneous USB DAQ device.

This project allows the user to control the devices through a command line interface. The user can enter initial settings, and then run a scan. The ***input frequency***, ***input voltage***, ***duration***, ***scan rate***, and ***scan mode*** are all user controlled.

Project was built using JetBrain PyCharm and Microsoft Visual Studio.

## Output

The output constists of 2 files and 1 window.
* ```output.txt``` - This file contains (scan_rate \*duration] elements that are the raw, 12 bit analog value received by the DAQ
* ```Final Output.txt``` - This file converts all elements in ```output.txt``` into voltage values based on ```scan mode```
* PyPlot window that graphs all elements in ```Final Output.txt```

## Prerequisites

**Here is what software you will need to use this software:**
* Windows - Due to the lack of drivers, this software only works in Windows.
* Hantek 1025G Drivers - You will have to get the Windows drivers for the generator. You will probably run into problems installing these drivers because they were poorly made.
* Measurement Computing InstaCal - This is the configuration for the Measurement Computing USB2020.

## Authors

* [**David Gurevich**](https://github.com/davidgur) - *All work so far*

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
