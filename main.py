from envirophat import light, motion, weather
from rdflib import Namespace, Graph, RDF, RDFS, XSD, URIRef, BNode, Literal

from etc import get_hash, get_iso_date
    
QUDT = Namespace('http://qudt.org/schema/qudt/')
SOSA = Namespace('http://www.w3.org/ns/sosa/')
CDT  = Namespace('https://w3id.org/cdt#')
PI   = Namespace('#')

class ObservationSnap(Graph):
    def __init__(self) -> None:
        super().__init__()
        self.bind('qudt', QUDT)
        self.bind('sosa', SOSA)
        self.bind('pi', PI)
        self.ts = Literal(get_iso_date(), datatype=XSD.dateTime)
        self.hash = get_hash(self.ts.toPython())
        self.add_sensors()

    def add_sensors(self):
        self.add_lights()
        self.add_acc()
        self.add_weather()


    def add_observation(self, name, value, u_uri, u_sym, sensor, property):
        obs = URIRef(f'{self.hash}#{name.lower()}', base=PI)
        bn = BNode()
        self.add((obs, RDF.type, SOSA.Observation))
        self.add((obs, SOSA.hasResult, bn))
        self.add((bn, QUDT.numericalValue, Literal(value)))
        self.add((bn, QUDT.unit, URIRef(u_uri)))
        self.add((obs, SOSA.hasSimpleResult, Literal(f'{value} {u_sym}', datatype=CDT.ucum)))
        self.add((obs, SOSA.madeBySensor, URIRef(f'sensors#{sensor}', base=PI)))
        self.add((obs, SOSA.observedProperty, URIRef(f'properties#{property}', base=PI)))
        self.add((obs, SOSA.resultTime, self.ts))

    def add_lights(self):
        lights = ('clear','red', 'green', 'blue')
        for i, val in enumerate(light.raw()):
            self.add_observation(name=lights[i],
                                 value=val,
                                 u_uri='http://qudt.org/vocab/unit#LUX',
                                 u_sym='lx',
                                 sensor='BMP280',
                                 property=f'Check{lights[i].capitalize()}')

    def add_acc(self):
        for i, mov in enumerate(motion.accelerometer()):
            self.add_observation(name=chr(120 + i),
                                 value=mov,
                                 u_uri='http://qudt.org/vocab/unit#G',
                                 u_sym='G',
                                 sensor='LSM303D',
                                 property=f'Direction{chr(88+i)}'
                                 )

    def add_weather(self):
        self.add_temp()
        self.add_pressure()
        self.add_altitude()

    
    def add_temp(self):
        self.add_observation(name='temperature',
                             value=weather.temperature(),
                             u_uri='http://qudt.org/vocab/unit#DEG_C',
                             u_sym='°C',
                             sensor='LSM303D',
                             property=f'CheckTemperature'
                            )

            
    def add_pressure(self):
        self.add_observation(name='pressure',
                             value=weather.pressure(unit='hPA'),
                             u_uri='http://qudt.org/vocab/unit#HectoPA',
                             u_sym='hPA',
                             sensor='BMP280',
                             property=f'CheckPressure'
                            )

    def add_altitude(self):
        self.add_observation(name='pressure',
                             value=weather.altitude(),
                             u_uri='http://qudt.org/vocab/unit#M',
                             u_sym='m',
                             sensor='BMP280',
                             property=f'CheckAltitude'
                            )

o = ObservationSnap()

print(o.serialize(format='ttl'))