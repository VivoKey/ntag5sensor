# NTAG 5 Sensor

Sensor reading for the NXP NTAG 5 Link, specifically with the Texas Instruments TMP117 sensors and the ACS ACR1552U PC/SC reader.

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

```
usage: ntag5sensor.py [-h] [-r [READER]] [-l]

Read NTAG 5 Link sensors

options:
  -h, --help            show this help message and exit
  -r [READER], --reader [READER]
                        index of the ACR1552 reader to use (default: 0)
  -l, --list-readers    list available ACR1552 readers
```

