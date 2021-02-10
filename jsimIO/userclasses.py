from .xmlnode_superclass import *
import lxml.etree as ET


class _UserClass(_XmlNode):
    def __init__(self, name, type, reference_station, priority):
        super().__init__("userClass")
        self.name = name
        self.type = type
        self.reference_station = reference_station
        self.priority = priority


class ClosedClass(_UserClass):  # da distribuire i parametri
    def __init__(self, name, customers, reference_station, priority=0):
        super().__init__(name, "closed", reference_station, priority)
        self.customers = customers


class OpenClass(_UserClass):
    def __init__(self, name, reference_station, distribution=None, priority=0):
        super().__init__(name, "open", reference_station, priority)
        self.distribution = distribution
