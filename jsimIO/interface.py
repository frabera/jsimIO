from .defaults import Default
from dataclasses import dataclass
from .distributions import _Distribution
from .strategies import _SchedStrategy
from .model import _Model
from .userclasses import _OpenClass, _ClosedClass
from .nodes import _Station, _Logger, _Source, _Sink
from .xmlnode_superclass import _XmlNode


# UTILS

class SchedStrategy:
    FCFS = "FCFS"


class Model:
    def __init__(self, name, options=Default.ModelOptions):
        self.name = name
        self.options = options
        self.userclasses = []
        self.nodes = []
        self.connections = []

    def set_routing(self, matrices):
        assert len(matrices) == len(
            self.userclasses), "The number of matrices must be equal \
                to the number of customer classes"
        #  normalizzare
        self.matrices = matrices


class Node:
    def __init__(self):
        self.classes_referenced = []


@dataclass
class OpenClass:
    model: Model
    name: str
    reference_station: Node
    distribution: _Distribution
    priority: int = 0

    def __post_init__(self):
        self.model.userclasses.append(self)


@dataclass
class ClosedClass:
    model: Model
    name: str
    customers: int
    reference_station: Node  # Serve?
    priority: int = 0

    def __post_init__(self):
        self.model.userclasses.append(self)


@dataclass
class Station(Node):
    model: Model
    name: str
    scheduling_strategy: str = SchedStrategy.FCFS  # da cambiare
    buffer_size: int = -1
    dropstrategy: str = "BAS blocking"  # da cambiare

    def __post_init__(self):
        self.model.nodes.append(self)
        self.service = []
        super().__init__()

    def set_service(self, userclass, distribution):
        self.service.append(
            {"userclass": userclass, "distribution": distribution})


@dataclass
class Source(Node):
    model: Model
    name: str

    def __post_init__(self):
        self.model.nodes.append(self)
        super().__init__()


@dataclass
class Sink(Node):
    model: Model
    name: str

    def __post_init__(self):
        self.model.nodes.append(self)
        super().__init__()


@dataclass
class Fork(Node):
    model: Model
    name: str

    def __post_init__(self):
        self.model.nodes.append(self)
        super().__init__()


@dataclass
class Join(Node):
    model: Model
    name: str

    def __post_init__(self):
        self.model.nodes.append(self)
        super().__init__()


@dataclass
class Logger(Node):
    model: Model
    name: str

    def __post_init__(self):
        self.model.nodes.append(self)
        super().__init__()


def link_classes_and_nodes(model):
    for node in model.nodes:
        node.classes_referenced = [
            userclass for userclass in model.userclasses
            if userclass.reference_station is node]


def bake(model):
    link_classes_and_nodes(model)
    baked_model = _Model(model.name, options=model.options)

    # Add Connections
    # model.connections = []
    for matrix in model.matrices:
        for source, row in enumerate(matrix):
            for target, probability in enumerate(row):
                if probability > 0:
                    model.connections.append(
                        (model.nodes[source].name, model.nodes[target].name))

    # Qui questione logger

    for connection in set(model.connections):
        baked_model.add_child(_XmlNode("connection", attributes={
            "source": connection[0],
            "target": connection[1]}))

    for node_index, node in enumerate(model.nodes):

        if isinstance(node, Source):
            node_E = baked_model.add_child(_Source(model, node.name))
            set_router(model, node_E.get_child(2), node_index)

        elif isinstance(node, Sink):
            node_E = baked_model.add_child(_Sink(model, node.name))

        #  ! random source per ogni nodo

        elif isinstance(node, Station):
            node_E = baked_model.add_child(_Station(
                baked_model, node.name, scheduling_strategy=node.scheduling_strategy,
                buffer_size=node.buffer_size, dropstrategy=node.dropstrategy))
            drop_strategy = node_E.get_child(0).add_child(
                _XmlNode("parameter",
                         attributes={
                             "array": "true",
                             "classPath": "java.lang.String",
                             "name": "dropStrategies"}))
            #  ! verificare che array sia true anche se una sola classe
            #  ! verificare se devo inserire solo le classi che passano
            #  ! dalla stazione o le posso mettere tutte
            for uc_index, userclass in enumerate(model.userclasses):
                # L'userclass passa dalla stazione
                if sum(model.matrices[uc_index][node_index]) > 0:
                    drop_strategy.add_child(
                        _XmlNode("refClass", text=userclass.name))
                    sub_par = drop_strategy.add_child(
                        _XmlNode("subParameter",
                                 attributes={"classPath": "java.lang.String",
                                             "name": "dropStrategy"}))
                    sub_par.add_child(
                        _XmlNode("value", text=node.dropstrategy))
            # SERVER
            server = node_E.get_child(1)
            max_jobs = server.add_child(_XmlNode("parameter",
                                                 attributes={
                                                     "classPath": "java.lang.Integer",
                                                     "name": "maxJobs"}))
            max_jobs.add_child(_XmlNode("value", text=1))
            service_strategy = server.add_child(
                _XmlNode("parameter", attributes={
                    "array": "true",
                    "classPath": "jmt.engine.NetStrategies.ServiceStrategy",
                    "name": "ServiceStrategy"}))
            for service in node.service:
                refclass = _XmlNode(
                    "refClass", text=service["userclass"].name)
                service_strategy.add_child(refclass)
                timestrategy = service_strategy.add_child(
                    _XmlNode("subParameter", attributes={
                        "classPath": "jmt.engine.NetStrategies.ServiceStrategies.ServiceTimeStrategy",
                        "name": "ServiceTimeStrategy"}))
                distribution_parameters_list = service["distribution"].get_elements_list(
                )
                for elem in distribution_parameters_list:
                    timestrategy._element.append(elem)

            # Router
            router = node_E.get_child(2)
            # da togliere node_index, si trova
            set_router(model, router, node_index)

    for userclass in model.userclasses:
        if isinstance(userclass, OpenClass):
            baked_model.add_child(_OpenClass(
                baked_model, userclass.name, userclass.reference_station.name,
                userclass.distribution, userclass.priority))
        elif isinstance(userclass, ClosedClass):
            baked_model.add_child(_ClosedClass(
                baked_model, userclass.name, userclass.customers,
                userclass.reference_station.name, userclass.priority))

    return baked_model


def set_router(model, router, node_index):
    routing_strategy = router.add_child(
        _XmlNode("parameter", attributes={
            "array": "true",
            "classPath": "jmt.engine.NetStrategies.RoutingStrategy",
            "name": "RoutingStrategy"}))
    for userclass_index, matrix in enumerate(model.matrices):
        if sum(matrix[node_index]) > 0:
            targets = [(index, prob) for index, prob in enumerate(
                matrix[node_index]) if prob > 0]
            routing_strategy.add_child(
                _XmlNode("refClass", text=model.userclasses[userclass_index].name))
            probabilities = routing_strategy.add_child(
                _XmlNode("subParameter", attributes={
                    "array": "true",
                    "classPath": "jmt.engine.NetStrategies.RoutingStrategies.EmpiricalStrategy",
                    "name": "Probabilities"}))
            empirical_entry = probabilities.add_child(
                _XmlNode("subParameter", attributes={
                    "array": "true",
                    "classPath": "jmt.engine.random.EmpiricalEntry",
                    "name": "EmpiricalEntryArray"}))
            for target in targets:
                empirical_entry.add_child(
                    _XmlNode("subParameter", attributes={
                        "classPath": "java.lang.String",
                        "name": "stationName"},
                        children=[_XmlNode("value", text=model.nodes[target[0]].name)]))
                empirical_entry.add_child(
                    _XmlNode("subParameter", attributes={
                        "classPath": "java.lang.Double",
                        "name": "probability"},
                        children=[_XmlNode("value", text=target[1])]))
