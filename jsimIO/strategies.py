from .xmlnode_superclass import *
from enum import Enum

# Scheduling


# class SchedStrategy(Enum):
class SchedStrategy:
    FCFS = 1


# Service


class ServiceStrategy(_XmlNode, Enum):
    # Load Independent
    ServiceTimeStrategy = 1


# Routing
