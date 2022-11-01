## Installing Enviro pHAT library and dependencies
You should install/update the sensor's library and dependencies. For that, type:

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

Stop the program with CTRL + C and clear the terminal:
```console
clear
```