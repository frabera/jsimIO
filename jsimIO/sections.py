from .xmlnode_superclass import *


class Section(XmlNode):
    def __init__(self, model):
        super().__init__("section")
        self.model = model


#  STATION
class Queue(Section):  # is a section
    def __init__(self, model, name, scheduling_strategy=None):
        super().__init__(model)
        print(model.__dict__)
        self.className = "Queue"


class Server(Section):
    def __init__(self, model, name, service_strategy=None):
        super().__init__(model)
        self.className = "Server"


class Router(Section):
    def __init__(self, model, name, routing_strategy=None):
        super().__init__(model)
        self.className = "Router"


#  SOURCE


#  SINK

# TODO Drop Strategies
