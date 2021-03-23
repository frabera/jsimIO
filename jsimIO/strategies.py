from .xmlnode_superclass import _Parameter


class SchedStrategy:
    class FCFS:
        def __repr__(self):
            return "FCFS"

        @staticmethod
        def _get_queueget_node():
            return _Parameter("jmt.engine.NetStrategies.QueueGetStrategies.FCFSstrategy",
                              "FCFSstrategy")


class DropStrategy:
    BAS_Blocking = "BAS blocking"


class QueuePutStrategy:
    TailStrategy = {
        "classPath": "jmt.engine.NetStrategies.QueuePutStrategies.TailStrategy",
        "name": "TailStrategy"
    }


# class _SchedStrategy:  # get? put? boh, tutto insieme
#     FCFS = {
#         "get":
#             {
#                 "classPath": "jmt.engine.NetStrategies.QueueGetStrategies.FCFSstrategy",
#                 "name": "FCFSstrategy"
#             },
#         "put":
#             {
#                 "array": "true",
#                 "classPath": "jmt.engine.NetStrategies.QueuePutStrategy",
#                 "name": "QueuePutStrategy"
#             },
#         "put_tail_subparam":
#             {
#                 "classPath": "jmt.engine.NetStrategies.QueuePutStrategies.TailStrategy",
#                 "name": "TailStrategy"
#             }
#     }


    def _get_queueget_node(self):
        return _Parameter("jmt.engine.NetStrategies.QueueGetStrategies.FCFSstrategy",
                          "FCFSstrategy")


# Service


class ServiceStrategy:
    # Load Independent
    ServiceTimeStrategy = 1


# class _Distribution(_XmlNode):
#     def __init__(self):
#         # Create service time xml node:
#         attributes = {
#             "array": "true",
#             "classPath": "jmt.engine.NetStrategies.ServiceStrategy",
#             "name": "ServiceStrategy"
#         }
#         super().__init__("parameter", attributes=attributes)

# Routing


class RoutingStrategy:
    Random = {
        "classPath": "jmt.engine.NetStrategies.RoutingStrategies.RandomStrategy",
        "name": "Random"
    }

    Probabilities = {

    }


class JoinStrategy:
    Standard = {
        "classPath": "jmt.engine.NetStrategies.JoinStrategies.NormalJoin",
        "name": "Standard Join"
    }

    Quorum = {
        "classPath": "jmt.engine.NetStrategies.JoinStrategies.PartialJoin",
        "name": "Quorum"
    }
