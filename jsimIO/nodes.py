from jsimIO.strategies import SchedStrategy
from .xmlnode_superclass import _XmlNode
from .sections import _Section, _Queue, _Router, _Server, _ServiceTunnel
from .defaults import *


class _Node(_XmlNode):
    def __init__(self, model):
        super().__init__("node")
        self.model_name = model._name  # !
        model.add_child(self)


class Station(_Node):  # Actually is a Queue
    def __init__(self, model, name,
                 scheduling_strategy=SchedStrategy.FCFS, buffer_size=-1, dropstrategy="drop"):
        super().__init__(model)
        self.name = name
        self.buffer_size = buffer_size
        self.scheduling_strategy = scheduling_strategy
        self.service_strategy = None
        self.routing_strategy = None
        self.add_child(_Queue(scheduling_strategy, buffer_size, dropstrategy))
        self.add_child(_Server())
        self.add_child(_Router())
        self.set_attributes({"name": self.name})

    def set_service(self, user_class, distribution):
        server = self.get_child(Id.Station.Server)
        max_jobs = server.add_child(_XmlNode("parameter", attributes={"classPath": "java.lang.Integer", "name": "maxJobs"}))
        max_jobs.add_child(_XmlNode("value", text=1))
        # number_of_visits = server.add_child(_XmlNode("parameter", attributes={"array":"true", "classPath":"java.lang.Integer", "name": "numberOfVisits"}))
        # number_of_visits.add_child(_XmlNode("refClass")) ignoro per il momento
        service_strategy = _XmlNode("parameter", attributes={"array":"true","classPath":"jmt.engine.NetStrategies.ServiceStrategy", "name":"ServiceStrategy"})
        refclass = _XmlNode("refClass", text=user_class.name)
        service_strategy.add_child(refclass)
        distribution_parameters_list = distribution.get_elements_list()
        for elem in distribution_parameters_list:
            # TODO cambiare dist in modo che ritorni dict e non list_xml
            service_strategy._element.append(elem)
        # Problema: parameter potrebbe già esistere, in tal caso devo aggiungere solo refclass e subpar
        # assunto che sia solo 1
        if server._element.find("parameter[@name='ServiceStrategy']"):
            server._element.find("parameter[@name='ServiceStrategy']").append(refclass._element)
            for elem in distribution_parameters_list:
                server._element.find("parameter[@name='ServiceStrategy']").append(elem)
        else:
            # discrepanza tra parameter._children e parameter._element
            server.add_child(service_strategy)




class Source(_Node):
    def __init__(self, model, name):
        super().__init__(model)
        self.name=name
        self.add_child(_Section("RandomSource"))
        self.add_child(_ServiceTunnel())
        self.add_child(_Router())

        self.set_attributes({"name": self.name})


class Sink(_Node):
    def __init__(self, model, name):
        super().__init__(model)
        self.name=name
        self.add_child(_Section("JobSink"))

        self.set_attributes({"name": self.name})


class Logger(_Node):
    def __init__(self, model, name):
        self.set_attributes({"name": self.name})
