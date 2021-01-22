from .xmlnode_superclass import *


class Section(XmlNode):
    def __init__(self, model, name, className):
        super().__init__("section")
        self.model = model
        self.name = name
        self.className = className


#  STATION
class Queue(Section):  # is a section
    def __init__(self, model, name, scheduling_strategy=None):
        super().__init__(model, name, "Queue")
        self.scheduling_strategy = scheduling_strategy


class Server(Section):
    def __init__(self, model, name, service_strategy=None):
        super().__init__(model, name, "Server")
        self.service_strategy = service_strategy


class Router(Section):
    def __init__(self, model, name, routing_strategy=None):
        super().__init__(model, name, "Router")
        self.routing_strategy = routing_strategy


#  SOURCE


#  SINK

# TODO Drop Strategies
