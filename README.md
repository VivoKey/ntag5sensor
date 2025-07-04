# NTAG 5 Sensor

Sensor reading for the `NXP NTAG 5 Link`, specifically with the `Texas Instruments TMP117` sensor and the `ACS ACR1552U` PC/SC reader.

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

You need to specify the I2C address of the connected TMP117 chip if it is not the default one. This address is determined by the ADD0 pin connection of the TMP117 chip.

Addresses:
 - `GND` (default): `72` (e.g. MikroElektronika)
 - `VCC`: `73` (e.g. Thermo)
 - `SDA`: `74` (e.g. Temptress)
 - `SCL`: `75`

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

usage: ntag5sensor.py tmp117 info [-h] [-r [READER]] [-a [{72,73,74,75}]]

options:
  -h, --help            show this help message and exit
  -r, --reader [READER]
                        index of the available ACR1552 readers to use (default: 0)
  -a, --address [{72,73,74,75}]
                        I2C address of the connected sensor chip (default: 72)

usage: ntag5sensor.py tmp117 setup [-h] [-r [READER]] [-a [{72,73,74,75}]] [-sm [{oneshot,continuous}]]

options:
  -h, --help            show this help message and exit
  -r, --reader [READER]
                        index of the available ACR1552 readers to use (default: 0)
  -a, --address [{72,73,74,75}]
                        I2C address of the connected sensor chip (default: 72)
  -sm, --startup-mode [{oneshot,continuous}]
                        Startup mode to configure the connected sensor chip with (default: oneshot)

usage: ntag5sensor.py tmp117 read [-h] [-r [READER]] [-a [{72,73,74,75}]] [-m [{oneshot,continuous}]]

options:
  -h, --help            show this help message and exit
  -r, --reader [READER]
                        index of the available ACR1552 readers to use (default: 0)
  -a, --address [{72,73,74,75}]
                        I2C address of the connected sensor chip (default: 72)
  -m, --mode [{oneshot,continuous}]
                        Mode to read the connected sensor chip in (default: oneshot)
```

