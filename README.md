# Description
Enviropi is a simple Flask application to serve semantically annotated sensor data for the [Raspberry Pi](https://www.raspberrypi.com/) and the [PIMORONI Enviro pHAT](http://docs.pimoroni.com/envirophat/). The application uses [RDFLib](https://rdflib.readthedocs.io/en/stable/index.html) to serialize data in Linked Data formats like JSON-LD or Turtle.

The [PIMORONI Enviro pHAT](http://docs.pimoroni.com/envirophat/) is an environmental sensor add-on consisting of an accelerometer, pressure, temperature, and light sensor.

Each sensor value is described as observation (according to the [SOSA ontology](http://www.w3.org/ns/sosa/)). Applied units are part of the [QUDT unit vocabulary](https://qudt.org/vocab/unit/).

The landing page provides an overview of all available RDF documents. __"newest.xxx"__ refers to the newest data snapshot. The application polls the sensor data regularly (~1s). __"data.xxx"__ refers to all acquired observations (100 newest timestamps).

Observations of a specific sensor can be isolated and displayed in a table. For that, use the attributes name, e.g. _temperature_ or _x_ (for the x-axis of the accelerometer). For the first example, the url would be:

[http://localhost:5000/table/temperature](http://localhost:5000/table/temperature)

## Installation
0. The prerequisite is to have an running raspberry pi. If you need to install an operating system first, see the [official website](https://www.raspberrypi.com/software/). The installation guide assumes you are working directly on the raspberry pi, but you could also configure the application via SSH connection.

1. Open your favorite terminal, move to the home directory, and clone the repository.
```console
cd ~
git clone https://github.com/wintechis/enviropi.git
```
2. Change directory to the repo folder.
```console
cd enviropi
```
3. Create a new virtual environment within this folder.
```console
python -m venv env
```
4. Activate the virtual environment (Windows example).
```console
env/scripts/activate
```
You should now see '(env)' at the start of the current input line of the terminal.

5. Install Flask (2.2.2), RDFLib (6.2.0), and Waitress (2.1.2). You can use also more recent versions, but the program was tested with the mentioned versions.
```console
pip install flask==2.2.2 rdflib==6.2.0 waitress=2.1.2
```
Congratulations! You have successfully installed all required packages.


# Running the application

## Run with Test Server
First, you want to make sure that the application can runs with Flask's test server.
```console
python main.py
```
Check, if the server responds to requests ([check](http://localhost:5000)).

## Run with Waitress
Next, check, if Waitress as the WSGI server works.
```console
waitress-serve --listen 0.0.0.0:5000 wsgi:app
```
Check, if the server responds to requests ([check](http://localhost:5000)).

## Run Service
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

Check, if the server responds to requests ([check](http://localhost:5000)).

# License
read [license](LICENSE)

* add flask instance
* serve single and all observations