from rdflib import Namespace, Graph, RDF, RDFS, XSD, URIRef, BNode, Literal
from rdflib.query import Result
import threading
import os
import time
from etc import FILES, REQUESTS
from observation import ObservationGraph

class DataPoll(threading.Thread):
    def __init__(self) -> None:
        super().__init__(daemon=True)
        self.singles = []
        self.all = ObservationGraph(first=True)

    def save_turtle(self, g: Graph, name: str) -> None:
        g.serialize(os.path.join(FILES, name), format='ttl')


    def reduce_all(self) -> None:
        # Each ObserverationGraph has 77 Triples
        if len(self.singles) > 77*100:
            last = self.singles.pop(0)
            self.all -= last

    def run(self) -> None:
        while True:
            time.sleep(1)
            o = ObservationGraph()
            self.singles.append(o)
            self.save_turtle(o, 'newest.ttl')

            self.all += o
            self.reduce_all()
            self.save_turtle(self.all, 'data.ttl')
        #return super().run()



if __name__ == '__main__':
    t = DataPoll()
    start = time.time()
    end = time.time() + 5
    t.start()

    while start < end:
        start = time.time()
        time.sleep(1)
    