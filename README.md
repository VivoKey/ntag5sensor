# NTAG 5 Sensor

Sensor reading for the `NXP NTAG 5 Link`, specifically with the `Texas Instruments TMP117` sensor and the `ACS ACR1552U` PC/SC reader.

For development hardware, use e.g. the MikroElektronika [NTAG 5 Link Click](https://www.mikroe.com/ntag-5-link-click) and [Thermo 11 Click](https://www.mikroe.com/thermo-11-click).

## Setup

Install [Python 3](https://www.python.org/downloads/) and Pip (usually packaged with Python), both are probably available via your package manager. Use Pip in the terminal to install the requirements, I suggest to use a virtual environment but it works just as well without one.

```
python3 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
``` 

You can also install the packages any other way you like, required modules are `pyscard`, `ber-tlv`. If you use Nix, Flake and EnvRC files are provided.

## Usage

A command-line interface is provided via the script `./ntag5sensor.py`.

### Select PC/SC reader

The script will automatically enumerate all connected compatible ACR ACR1552U readers. To list the detected readers, run

```
./ntag5sensor.py -l
```

Afterwards, select the index of the reader you want to use (if it is not the default 0 one), by using the `-r` flag.

### TMP117 I2C address

You need to specify the I2C address of the connected TMP117 chip if it is not the default one, by using the `-a` flag. This address is determined by the ADD0 pin connection of the TMP117 chip.

ADD0 connection and the resulting I2C address:
 - `GND` (default): `72` (e.g. [MikroElektronika Thermo 11 Click](https://www.mikroe.com/thermo-11-click))
 - `VCC`: `73` (e.g. Thermo)
 - `SDA`: `74` (e.g. [Temptress](https://github.com/LitAF-RFID/Temptress))
 - `SCL`: `75`

### Example

This assumes you have an assembly with the factory default configuration. The parameters here use their default values and are only included for illustration, they would also default to these values if omitted. First, inspect the configuration:

```
./ntag5sensor.py info
```

Then, setup the NTAG5 Link, by modifying its internal persistent configuration store. This automatically enables SRAM and I2C master mode, and applies the specified current and voltage configurations for energy harvesting. The default is `0.4` mA and `1.8` V. Afterwards, you can confirm your changes have been applied by running the `info` action again.

```
./ntag5sensor.py setup -c 0.4 -v 1.8
./ntag5sensor.py info
```

Next, make sure you can query the connected TMP117 sensor. Do not forget to specify the `-a` I2C address if needed:

```
./ntag5sensor.py tmp117 info -a 72
```

Now, setup the persistent configuration of the connected TMP117 sensor. This example uses the default average and cycle timings, and puts the sensor in one-shot (shutdown) mode at boot.

```
./ntag5sensor.py tmp117 setup -a 72 -av 8 -cy 4 -mo oneshot
./ntag5sensor.py tmp117 info -a 72
```

Finally, you can read out the measurements from the sensor. This step is the only one you will need to run in the future, as the previous setting are applied persistently. You can specify a different mode than the one applied during sensor boot via the persistent configuration, the script will then switch the mode using the transient runtime configuration.

```
./ntag5sensor.py tmp117 read -mo oneshot
```

### Command reference

```
usage: ntag5sensor.py [-h] [-hd] [-l] {info,setup,tmp117} ...

Read and configure sensors connected to NTAG 5 Link

positional arguments:
  {info,setup,tmp117}   desired action to perform
    info                read information and configuration data of the NTAG5 Link
    setup               write persistent configuration settings into the NTAG5 Link EEPROM
    tmp117              manage connected TMP117 sensor

options:
  -h, --help            show this help message and exit
  -hd, --help-documentation
                        Print the complete help documentation
  -l, --list-readers    list available ACR1552 readers

usage: ntag5sensor.py info [-h] [-r [READER]]

options:
  -h, --help            show this help message and exit
  -r, --reader [READER]
                        index of the available ACR1552 readers to use (default: 0)

usage: ntag5sensor.py setup [-h] [-r [READER]] [-c [{0.4,0.6,1.4,2.7,4.0,6.5,9.0,12.5}]] [-v [{1.8,2.4,3.0}]]

options:
  -h, --help            show this help message and exit
  -r, --reader [READER]
                        index of the available ACR1552 readers to use (default: 0)
  -c, --current [{0.4,0.6,1.4,2.7,4.0,6.5,9.0,12.5}]
                        minimum available current for energy harvesting to trigger, in mA (default: 0.4)
  -v, --voltage [{1.8,2.4,3.0}]
                        regulated voltage output of active energy harvesting, in V (default: 1.8)

usage: ntag5sensor.py tmp117 [-h] {info,setup,read} ...

positional arguments:
  {info,setup,read}  desired action to perform on the connected TMP117 sensor
    info             read information and configuration of the connected TMP117 sensor
    setup            write persistent configuration to the connected TMP117 sensor
    read             read measurement data from the connected TMP117 sensor

options:
  -h, --help         show this help message and exit

usage: ntag5sensor.py tmp117 info [-h] [-r [READER]] [-a [{72,73,74,75}]]

options:
  -h, --help            show this help message and exit
  -r, --reader [READER]
                        index of the available ACR1552 readers to use (default: 0)
  -a, --address [{72,73,74,75}]
                        I2C address of the connected sensor chip (default: 72)

usage: ntag5sensor.py tmp117 setup [-h] [-r [READER]] [-a [{72,73,74,75}]] [-mo [{oneshot,continuous}]] [-av [{1,8,32,64}]] [-cy [{0,1,2,3,4,5,6,7}]]

options:
  -h, --help            show this help message and exit
  -r, --reader [READER]
                        index of the available ACR1552 readers to use (default: 0)
  -a, --address [{72,73,74,75}]
                        I2C address of the connected sensor chip (default: 72)
  -mo, --mode [{oneshot,continuous}]
                        Mode to operate the connected sensor chip in (default: oneshot)
  -av, --average [{1,8,32,64}]
                        Number of internal samples to average over (default: 8)
  -cy, --cycle [{0,1,2,3,4,5,6,7}]
                        Cycle timing mode in continuous mode, see table 7-7 (default: 4)

usage: ntag5sensor.py tmp117 read [-h] [-r [READER]] [-a [{72,73,74,75}]] [-mo [{oneshot,continuous}]]

options:
  -h, --help            show this help message and exit
  -r, --reader [READER]
                        index of the available ACR1552 readers to use (default: 0)
  -a, --address [{72,73,74,75}]
                        I2C address of the connected sensor chip (default: 72)
  -mo, --mode [{oneshot,continuous}]
                        Mode to operate the connected sensor chip in (default: oneshot)
```

