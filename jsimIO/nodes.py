from jsimIO.strategies import SchedStrategy
from .xmlnode_superclass import *
from .sections import *


class _Node(_XmlNode):
    def __init__(self, model):
        super().__init__("node")
        self.model = model
        model._children.append(self)


class Station(_Node):  # Actually is a Queue
    def __init__(self, model, name,
                 scheduling_strategy=SchedStrategy.FCFS, buffersize=-1):
        super().__init__(model)
        self.name = name
        self.buffersize = buffersize
        self.scheduling_strategy = scheduling_strategy
        self.service_strategy = None
        self.routing_strategy = None
        self._children.extend([_Queue(model, name, scheduling_strategy), _Server(model, name), _Router(model, name)])


class Source(_Node):
    def __init__(self, model, name):
        super().__init__(model)
        self.name = name


class Sink(_Node):
    def __init__(self, model, name):
        super().__init__(model)
        self.name = name


class Logger(_Node):
    def __init__(self, model, name):
        pass
