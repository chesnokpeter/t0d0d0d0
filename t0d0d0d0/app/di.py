import punq

import abc

cont = punq.Container()


class AbsConnector(abc.ABC):
    @abc.abstractmethod
    def connect(self):
        raise NotImplementedError
    

class HelloConnector(AbsConnector):
    def __init__(self):
        print('init...')
    def connect(self):
        print('connect to hello ...')

cont.register(AbsConnector, HelloConnector, scope=punq.Scope.singleton)

conn = cont.resolve(AbsConnector)

conn.connect()
conn.connect()
conn.connect()
conn.connect()
