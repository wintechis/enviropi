# EnviroPi - Web application to serve smenatically annotated sensor data
Enviropi is a simple Flask application to serve semantically annotated sensor data for the [Raspberry Pi](https://www.raspberrypi.com/) and the [PIMORONI Enviro pHAT](http://docs.pimoroni.com/envirophat/). The application uses [RDFLib](https://rdflib.readthedocs.io/en/stable/index.html) to serialize data in Linked Data formats like JSON-LD or Turtle.

The [PIMORONI Enviro pHAT](http://docs.pimoroni.com/envirophat/) is an environmental sensor add-on consisting of an accelerometer, pressure, temperature, and light sensor.

Each sensor value is described as observation (according to the [SOSA ontology](http://www.w3.org/ns/sosa/)). Applied units are part of the [QUDT unit vocabulary](https://qudt.org/vocab/unit/).

The landing page provides an overview of all available RDF documents. __"newest.xxx"__ refers to the newest data snapshot. The application polls the sensor data regularly (~1s). __"data.xxx"__ refers to all acquired observations (100 newest timestamps).

Observations of a specific sensor can be isolated and displayed in a table. For that, use the attributes name, e.g. _temperature_ or _x_ (for the x-axis of the accelerometer). For the first example, the url would be:

[http://localhost:5000/table/temperature](http://localhost:5000/table/temperature)

## Installation

## Booting Raspberry

The first prerequisite is to have a running raspberry pi. If you need to install an operating system first, see the [official website](https://www.raspberrypi.com/software/). The installation guide assumes that you configure the application via SSH connection.

In the settings of the Raspberry Pi Imager, you can set up a hostname, SSH credentials and Wifi settings. Doing so, there is no need to connect the Raspbbery with a keyboard or display. In this installation guide the following settings were made:
* hostname: enviropi.local
* user: pi
* Enable SSH (decide a PW on your own)
* Set Wifi (set your local Wifi configurations)

Before powering your raspbbery on, connect the environment sensor according to the [pinout](https://pinout.xyz/pinout/enviro_phat). After you are done, put the SD card into the raspberry slot and power the raspberry. The operating system is automatically installed. This can take a while.

You can check with your terminal, if your raspberry is done installing, by pinging it
```console
ping enviropi.local
```
When you receive responses, you can proceed.

### Establishing a SSH connection
From now on, you must work on the raspberry. For that, you must establish a SSH connection. Open your preferred terminal (e.g., PowerShell) and type:

```console
ssh pi@enviropi.local
```
You should now see that the line starts with _pi@envirpi:_.

### Enabling I2C
The I2C protocol is not automatically enabled. To do so, type:
```console
sudo raspi-config nonint do_i2c 0
```

To check, if the I2C connection is working, type:
```console
i2cdetect -y 1
```

You should see the following ouput:
```console
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:                         -- -- -- -- -- -- -- -- 
10: -- -- -- -- -- -- -- -- -- -- -- -- -- 1d -- --
20: -- -- -- -- -- -- -- -- -- 29 -- -- -- -- -- -- 
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
40: -- -- -- -- -- -- -- -- -- 49 -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- 77
```
If you do only see dashes and no hexcode, the sensor might not be connected correctly.

### Installing Enviro pHAT library and dependencies
Next step, you should install/update the sensor's library and dependencies. For that, type:

```console
curl https://get.pimoroni.com/envirophat | bash
```

This download might take a while. Agree to download the full installation including examples. After the download is complete, you can run one of the examples to check if the sensor is working:
```console
python /home/pi/Pimoroni/envirophat/examples/all.py
```

The output should look similar to the content of the box below. However, values should be different.
```console
Altitude: 274.41m
Light: 2
RGB: 127, 127, 127
Heading: 266.71
Magnetometer: 27 -9782 -3042
Accelerometer: -0.1g 0.02g -0.94g
Analog: 0: 0.519, 1: 0.519, 2: 0.537, 3: 0.549
```

### Cloning Repository
0. Before you can clone the repository, you must generate a [token](https://github.com/settings/tokens) that allows repo actions. If you do not plan to work with the raspberry later, just let the token expire on the next day.

1. Within the SSH-connection, type:
```console
clear
cd ~
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