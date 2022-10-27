from typing import Tuple
import random



class cls_light:
    def rgb(self) -> Tuple[int]:
        return (random.randrange(0,256),
                random.randrange(0,256),
                random.randrange(0,256)
            )

    def light(self) -> int:
        return random.randrange(0,256)
    
    def raw(self):
        return (self.light(), *self.rgb())
    

class cls_leds:
    def __init__(self, status=0):
        self.status = status

    def on(self) -> bool:
        self.status = 1
        return True

    def off(self) -> None:
        self.status = 0

    def is_on(self) -> bool:
        if self.status == 1:
            return True
        else:
            return False

    def is_off(self) -> bool:
        if self.status == 0:
            return True
        else:
            return False


class cls_weather:
    def temperature(self) -> float:
        """returns temperature between 18 and 25"""
        return round(random.uniform(18, 25), 1)

    def pressure(self, unit=None) -> float:
        """returns pressure in hPA between 1013.25 and 1050"""
        p = round(random.uniform(1013.25, 1050.0), 1)
        if unit is None:
            unit = "Pa"
        if unit.lower() == "hpa":
            return p 
        else:
            return p * 100

    def altitude(self, qnh=1013.25) -> int:
        """Return the current approximate altitude."""
        return 44330.0 * (1.0 - pow(self.pressure() / (qnh*100), (1.0/5.255)))

class cls_motion:
    def magnetometer(self):
        return self.accelerometer()

    def accelerometer(self):
        return (random.randint(-128, 127),
                random.randint(-128, 127),
                random.randint(-128, 127)
            )

    def heading(self):
        return random.randint(0, 360)

    def raw_heading(self):
        return self.heading()

    def update(self):
        pass

light = cls_light()
leds = cls_leds()
weather = cls_weather()
motion = cls_motion()