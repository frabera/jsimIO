from .xmlnode_superclass import *


class _Section(_XmlNode):
    def __init__(self, model, name, className):
        super().__init__("section")
        self.model = model
        self.name = name
        self.className = className


#  STATION
class _Queue(_Section):  # is a section
    def __init__(self, model, name, scheduling_strategy=None):
        super().__init__(model, name, "Queue")
        self.scheduling_strategy = scheduling_strategy


class _Server(_Section):
    def __init__(self, model, name, service_strategy=None):
        super().__init__(model, name, "Server")
        self.service_strategy = service_strategy


class _Router(_Section):
    def __init__(self, model, name, routing_strategy=None):
        super().__init__(model, name, "Router")
        self.routing_strategy = routing_strategy


#  SOURCE


#  SINK

# TODO Drop Strategies
