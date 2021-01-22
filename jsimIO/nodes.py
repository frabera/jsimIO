from jsimIO.strategies import SchedStrategy
from .xmlnode_superclass import *
from .sections import *


class Node(XmlNode):
    def __init__(self, model):
        super().__init__("node")
        self.model = model
        model._children.append(self)


class Station(Node):  # Actually is a Queue
    def __init__(self, model, name,
                 scheduling_strategy=SchedStrategy.FCFS, buffersize=-1):
        super().__init__(model)
        self.name = name
        self.buffersize = buffersize
        self.scheduling_strategy = scheduling_strategy
        self.service_strategy = None
        self.routing_strategy = None
        self._children.append(Queue(model, name, scheduling_strategy),
                              Server(model, name),
                              Router(model, name))


class Source(Node):
    def __init__(self, model, name):
        super().__init__(model)
        self.name = name


class Sink(Node):
    def __init__(self, model, name):
        super().__init__(model)
        self.name = name


class Logger(Node):
    def __init__(self, model, name):
        pass
