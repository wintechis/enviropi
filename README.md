![Demonstration](docs/enviropi.gif)

![Supported Python Versions](https://img.shields.io/badge/python-3.9-blue.svg)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

# EnviroPi - Web application to serve semantically annotated sensor data
Enviropi is a simple Flask application to serve semantically annotated sensor data for the [Raspberry Pi](https://www.raspberrypi.com/) and the [PIMORONI Enviro pHAT](http://docs.pimoroni.com/envirophat/). The application uses [RDFLib](https://rdflib.readthedocs.io/en/stable/index.html) to serialize data in Linked Data formats like JSON-LD or Turtle.

The [PIMORONI Enviro pHAT](http://docs.pimoroni.com/envirophat/) is an environmental sensor add-on consisting of an accelerometer, pressure, temperature, and light sensor.

Each sensor value is described as observation (according to the [SOSA ontology](http://www.w3.org/ns/sosa/)). Applied units are part of the [QUDT unit vocabulary](https://qudt.org/vocab/unit/).

The landing page provides an overview of all available RDF documents. __"newest.xxx"__ refers to the newest data snapshot. The application polls the sensor data regularly (~1s). __"data.xxx"__ refers to all acquired observations (100 newest timestamps).

Observations of a specific sensor can be isolated and displayed in a table. For that, use the attributes name, e.g. _temperature_ or _x_ (for the x-axis of the accelerometer). For the first example, the url would be:

* [http://localhost:5000/table/temperature](http://localhost:5000/table/temperature)(if working on the raspberry)
* [http://enviropi.local:5000/table/temperature](http://enviropi.local:5000/table/temperature)(if accessing from other machine)

The project contains a [mockup file](mock_envirophat.py) for the sensor, if you want to test the application on your computer before running it on the Raspberry Pi. The mockup is used when the original enviro pHAT library is not installed (which is always the case when executed on another platform than Raspberry Pi OS).

## Installation

### Preparation
Before you proceed, make sure that you [set up the raspberry pi correctly](docs/SETUP.md), [enabled the I2C protocol](docs/I2C.md), and [installed the Enviro pHat library and dependencies](docs/DEPEND.md). 

### Cloning Repository
0. Before you can clone the repository, you must generate a [token](https://github.com/settings/tokens) that allows repo actions. If you do not plan to work with the raspberry later, just let the token expire on the next day. The token will be used as the password when asked for it.

1. Within the SSH-connection and in home directory, type:
```console
git clone https://github.com/wintechis/enviropi.git
```
2. Change directory to the repo folder.
```console
cd enviropi
```

3. Install Flask (2.2.2), RDFLib (6.2.0), and Waitress (2.1.2). You can use also more recent versions, but the program was tested with the mentioned versions.
```console
pip install flask==2.2.2 rdflib==6.2.0 waitress==2.1.2
```

4. Note that this installation guide is not using a virtual environment. The reason for this is that the Python3-smbus library must be set up manually, if a virtal environment is used. The trade-off is that waitress-serve cannot be invoked directly, because the .local path is not global. Therefore, type:

```console
export PATH=/home/pi/.local/bin:$PATH
```

Congratulations! You have successfully installed all required packages.


## Running the application

### Run with Test Server
First, you want to make sure that the application can runs with Flask's test server.
```console
python main.py
```
Check, if the server responds to requests ([check](http://enviropi.local:5000)).

### Run with Waitress
Next, check, if Waitress as the WSGI server works.
```console
waitress-serve --listen 0.0.0.0:5000 wsgi:app
```
Check, if the server responds to requests ([check](http://enviropi.local:5000)).

### Run Service
At last, set up a service to run the application permanently. For that, move the service file to the system folder. If your user name is not "pi", your project is not named "enviropi", or you did not save the project on home level, you must edit the service file.

```console
sudo mv enviropi.service /etc/systemd/system/
```

Start, enable, and check the status of your configured service.
```console
sudo systemctl start enviropi
sudo systemctl enable enviropi
sudo systemctl status enviropi
```

If your service is running, the status message should include a line with _'Active: active (running) ...'_

Check, if the server responds to requests ([check](http://enviropi.local:5000)).

At last, you can also restart the pi to confirm that the service automatically starts. The application is now completely configured.

# License
read [license](LICENSE)