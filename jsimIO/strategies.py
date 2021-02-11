from .xmlnode_superclass import _XmlNode
from enum import Enum

# Scheduling


# class SchedStrategy(Enum):
class SchedStrategy:  # get? put? boh, tutto insieme
    FCFS = {
        "get":
            {
                "classPath": "jmt.engine.NetStrategies.QueueGetStrategies.FCFSstrategy",
                "name": "FCFSstrategy"
            },
        "put":
            {
                "array": "true",
                "classPath": "jmt.engine.NetStrategies.QueuePutStrategy",
                "name": "QueuePutStrategy"
            },
        "put_tail_subparam":
            {
                "classPath": "jmt.engine.NetStrategies.QueuePutStrategies.TailStrategy",
                "name": "TailStrategy"
            }
    }


# Service


class ServiceStrategy:
    # Load Independent
    ServiceTimeStrategy = 1


# Routing

# Drop Strategies
