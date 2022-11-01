## Enabling I2C
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