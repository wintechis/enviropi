## Setting up the Raspberry Pi

The first prerequisite is to have a running raspberry pi. If you need to install an operating system first, see the [official website](https://www.raspberrypi.com/software/). The installation guide assumes that you configure the application via SSH connection. This guide used an Raspberry Pi Zero W.

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
