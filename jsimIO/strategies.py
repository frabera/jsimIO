from .xmlnode_superclass import *
from enum import Enum

# Scheduling


class SchedStrategy(Enum):
    FCFS = 1


# Service


class ServiceStrategy(XmlNode, Enum):
    # Load Independent
    ServiceTimeStrategy = 1


# Routing
