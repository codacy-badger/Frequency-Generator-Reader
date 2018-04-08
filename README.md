# Frequency Generator and Reader

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/a7f6ffc1e54c4987857f00c48a3705c7)](https://app.codacy.com/app/davidgur/Frequency-Generator-Reader?utm_source=github.com&utm_medium=referral&utm_content=davidgur/Frequency-Generator-Reader&utm_campaign=badger)

The currently unnamed frequency generator and reader, which, upon completion will be used in CrossFlow utilities in industrial applications.

It interacts with the Hantek 1025G 25MHz Arbitrary function generator as well as the Measurement Computing USB 2020 high-speed simultaneous USB DAQ device.

This project allows the user to control the devices through a command line interface. The user can enter initial settings, and then run a scan. The ***input frequency***, ***input voltage***, ***duration***, ***scan rate***, and ***scan mode*** are all user controlled.

This project was built using [Atom](http://atom.io).

## Output

The output consists of 3 files and 1 window.
* ```output.txt``` - This file contains (scan_rate \*duration] elements that are the raw, 12 bit analog value received by the DAQ
* ```voltage output.txt``` - This file converts all elements in ```output.txt``` into voltage values based on ```scan mode```
* ```OutputPlot.png``` - This is a PyPlot that graphs the elements in ```voltage output.txt```
* PyPlot window that graphs all elements in ```voltage output.txt```

## Running the Software

**Prerequisites:**
* Windows - Due to the lack of drivers, this software only works in Windows.
* Hantek 1025G Drivers - You will have to get the Windows drivers for the generator. You will probably run into problems installing these drivers because they were poorly made and I hate them.
* Measurement Computing InstaCal - This is the configuration software for the Measurement Computing USB2020.

**Actually running the software:**

Simply execute ```scan.py```



## Authors

* [**David Gurevich**](https://github.com/davidgur) - *All work so far*

## License

This work is licensed under the Creative Commons Attribution-NonCommercial-NoDerivs 3.0 Unported License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-nd/3.0/ or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

![image](https://i.creativecommons.org/l/by-nc-nd/3.0/88x31.png)
