from .strategies import _SchedStrategy
from .xmlnode_superclass import _XmlNode
from .sections import _Section, _Queue, _Router, _Server, _ServiceTunnel
from .defaults import *


class _Node(_XmlNode):
    def __init__(self, model):
        super().__init__("node")
        # self.model_name = model._name  # !
        # model.add_child(self)

    def route(self, userclass, target, probability):
        pass


class _Station(_Node):  # Actually is a Queue
    def __init__(self, model, name,
                 scheduling_strategy=_SchedStrategy.FCFS, buffer_size=-1, dropstrategy="BAS blocking"):
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
        max_jobs = server.add_child(_XmlNode("parameter", attributes={
                                    "classPath": "java.lang.Integer", "name": "maxJobs"}))
        max_jobs.add_child(_XmlNode("value", text=1))
        # number_of_visits = server.add_child(_XmlNode("parameter", attributes={"array":"true", "classPath":"java.lang.Integer", "name": "numberOfVisits"}))
        # number_of_visits.add_child(_XmlNode("refClass")) ignoro per il momento
        service_strategy = _XmlNode("parameter", attributes={
                                    "array": "true", "classPath": "jmt.engine.NetStrategies.ServiceStrategy", "name": "ServiceStrategy"})
        refclass = _XmlNode("refClass", text=user_class.name)
        service_strategy.add_child(refclass)
        distribution_parameters_list = distribution.get_elements_list()
        for elem in distribution_parameters_list:
            # TODO cambiare dist in modo che ritorni dict e non list_xml
            service_strategy._element.append(elem)
        # Problema: parameter potrebbe già esistere, in tal caso devo aggiungere solo refclass e subpar
        # assunto che sia solo 1
        if server._element.find("parameter[@name='ServiceStrategy']"):
            server._element.find(
                "parameter[@name='ServiceStrategy']").append(refclass._element)
            for elem in distribution_parameters_list:
                server._element.find(
                    "parameter[@name='ServiceStrategy']").append(elem)
        else:
            # discrepanza tra parameter._children e parameter._element
            server.add_child(service_strategy)


class _Source(_Node):
    def __init__(self, model, name):
        super().__init__(model)
        self.name = name
        self.add_child(_Section("RandomSource"))
        self.add_child(_ServiceTunnel())
        self.add_child(_Router())

        self.set_attributes({"name": self.name})


class _Sink(_Node):
    def __init__(self, model, name):
        super().__init__(model)
        self.name = name
        self.add_child(_Section("JobSink"))

        self.set_attributes({"name": self.name})


class _Logger(_Node):
    def __init__(self, model, name):
        super.__init__(model)
        self.name = name
        self.set_attributes({"name": self.name})
        # DA RIVEDERE I PARAMETRI
        queue = self.add_child(_Queue("DA RIFARE", -1, "BAS Blocking"))
        drop_strategy = node_E.get_child(0).add_child(
            _XmlNode("parameter",
                     attributes={
                         "array": "true",
                         "classPath": "java.lang.String",
                         "name": "dropStrategies"}))
        node_E.get_child(0).add_child(  # get queue strategy
            _XmlNode("parameter",
                     attributes={
                         "classPath": "jmt.engine.NetStrategies.QueueGetStrategies.FCFSstrategy",
                         "name": "FCFSstrategy"}))
        put_queue_strategy = node_E.get_child(0).add_child(
            _XmlNode("parameter",
                     attributes={
                         "array": "true",
                         "classPath": "jmt.engine.NetStrategies.QueuePutStrategy",
                         "name": "QueuePutStrategy"}))

        #  ! verificare che array sia true anche se una sola classe
        #  ! verificare se devo inserire solo le classi che passano
        #  ! dalla stazione o le posso mettere tutte
        for uc_index, userclass in enumerate(model.userclasses):
            # L'userclass passa dalla stazione
            # if sum(model.matrices[uc_index][node_index]) > 0:
            # se rimetto l'if va indentato +1
            # vuole dropstrategy per tutte le classi

            # DROP STRATEGY
            drop_strategy.add_child(
                _XmlNode("refClass", text=userclass.name))
            sub_par = drop_strategy.add_child(
                _XmlNode("subParameter",
                         attributes={"classPath": "java.lang.String",
                                     "name": "dropStrategy"}))
            sub_par.add_child(
                _XmlNode("value", text=node.dropstrategy))

            # QUEUE STRATEGY
            put_queue_strategy.add_child(
                _XmlNode("refClass", text=userclass.name))
            put_queue_strategy.add_child(
                _XmlNode("subParameter",
                         attributes={
                             "classPath": "jmt.engine.NetStrategies.QueuePutStrategies.TailStrategy",
                             "name": "TailStrategy"}))
