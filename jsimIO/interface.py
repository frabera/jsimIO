from .distributions import *
from .model import *
from .userclasses import *
from .nodes import *
from .xmlnode_superclass import _XmlNode


def link_classes_and_nodes(model):
    for node in model.nodes:
        node.classes_referenced = [
            userclass for userclass in model.userclasses
            if userclass.reference_station is node]


def add_logger(baked_model, node):
    baked_model.add_child(_Logger(baked_model, f"LOG_{node.name}"))


def bake(model, fill_loggers=True):

    link_classes_and_nodes(model)
    baked_model = model

    # Add userclasses TAGS
    add_userclass_elements(model, baked_model)

    # Add nodes TAGs
    for node_index, node in enumerate(model.nodes):

        if isinstance(node, Source):
            node_E = baked_model.add_child(_Source(model, node.name))
            userclasses_referenced = [
                userclass for userclass in model.userclasses if userclass.reference_station is node]
            # Userclass solo open
            if len(userclasses_referenced) > 0:
                source_service_strategy = node_E.get_child(0).add_child(
                    _XmlNode("parameter", attributes={
                        "array": "true",
                        "classPath": "jmt.engine.NetStrategies.ServiceStrategy",
                        "name": "ServiceStrategy"}))
                for userclass_source in userclasses_referenced:
                    refclass = _XmlNode(
                        "refClass", text=userclass_source.name)
                    source_service_strategy.add_child(refclass)
                    timestrategy = source_service_strategy.add_child(
                        _XmlNode("subParameter", attributes={
                            "classPath": "jmt.engine.NetStrategies.ServiceStrategies.ServiceTimeStrategy",
                            "name": "ServiceTimeStrategy"}))
                    distribution_parameters_list = userclass_source.distribution.get_elements_list()
                    for elem in distribution_parameters_list:
                        timestrategy._element.append(elem)

            set_router(model, node_E.get_child(2), node_index)

        elif isinstance(node, Sink):
            node_E = baked_model.add_child(_Sink(model, node.name))

            # Logger
            logger_node = baked_model.add_child(
                _XmlNode("node", attributes={"name": f"LOG_{node.name}"}))
            queue_section = logger_node.add_child(
                _XmlNode("section", attributes={"className": "Queue"}))
            size = queue_section.add_child(_XmlNode("parameter", attributes={
                "classPath": "java.lang.Integer", "name": "size"}))
            size.add_child(_XmlNode("value", text=-1))
            drop_strategy = queue_section.add_child(_XmlNode("parameter", attributes={
                "array": "true",
                "classPath": "java.lang.String",
                "name": "dropStrategies"
            }))
            queue_section.add_child(  # get queue strategy
                _XmlNode("parameter",
                         attributes={
                             "classPath": "jmt.engine.NetStrategies.QueueGetStrategies.FCFSstrategy",
                             "name": "FCFSstrategy"}))
            put_queue_strategy = queue_section.add_child(
                _XmlNode("parameter",
                         attributes={
                             "array": "true",
                             "classPath": "jmt.engine.NetStrategies.QueuePutStrategy",
                             "name": "QueuePutStrategy"}))
            for userclass in model.userclasses:
                drop_strategy.add_child(
                    _XmlNode("refClass", text=userclass.name))
                sub_par = drop_strategy.add_child(
                    _XmlNode("subParameter",
                             attributes={"classPath": "java.lang.String",
                                         "name": "dropStrategy"}))
                sub_par.add_child(
                    _XmlNode("value", text="BAS blocking"))

                # QUEUE STRATEGY
                put_queue_strategy.add_child(
                    _XmlNode("refClass", text=userclass.name))
                put_queue_strategy.add_child(
                    _XmlNode("subParameter",
                             attributes={
                                 "classPath": "jmt.engine.NetStrategies.QueuePutStrategies.TailStrategy",
                                 "name": "TailStrategy"}))

            logtunnel_section = logger_node.add_child(
                _XmlNode("section", attributes={"className": "LogTunnel"}))
            logtunnel_section.add_child(_XmlNode("parameter", children=[_XmlNode("value", text="global.csv")], attributes={
                "classPath": "java.lang.String",
                "name": "logfileName"
            }))
            logtunnel_section.add_child(_XmlNode("parameter", children=[_XmlNode("value", text=baked_model.path_folder)], attributes={
                "classPath": "java.lang.String",
                "name": "logfilePath"
            }))
            for bool_param in ["logExecTimestamp", "logLoggerName", "logTimeStamp", "logJobID", "logJobClass", "logTimeSameClass", "logTimeAnyClass"]:
                logtunnel_section.add_child(_XmlNode("parameter", children=[_XmlNode("value", text="true")], attributes={
                    "classPath": "java.lang.Boolean",
                    "name": bool_param
                }))
            logtunnel_section.add_child(_XmlNode("parameter", children=[_XmlNode("value", text=len(model.userclasses))], attributes={
                "classPath": "java.lang.Integer",
                "name": "numClasses"
            }))

            router_section = logger_node.add_child(
                _XmlNode("section", attributes={"className": "Router"}))
            routing_strategy = router_section.add_child(_XmlNode("parameter", attributes={
                "array": "true",
                "classPath": "jmt.engine.NetStrategies.RoutingStrategy",
                "name": "RoutingStrategy"
            }))
            for userclass in model.userclasses:
                routing_strategy.add_child(
                    _XmlNode("refClass", text=userclass.name))
                routing_strategy.add_child(_XmlNode("subParameter", attributes={
                    "classPath": "jmt.engine.NetStrategies.RoutingStrategies.RandomStrategy",
                    "name": "Random"
                }))

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
            # SERVER
            server = node_E.get_child(1)
            max_jobs = server.add_child(_XmlNode("parameter",
                                                 attributes={
                                                     "classPath": "java.lang.Integer",
                                                     "name": "maxJobs"}))
            max_jobs.add_child(_XmlNode("value", text=1))

            # qui number of visits che PARE INUTILE
            number_of_visits = server.add_child(
                _XmlNode("parameter", attributes={
                    "array": "true",
                    "classPath": "java.lang.Integer",
                    "name": "numberOfVisits"}))
            # for service in node.service:
            #     refclass = _XmlNode(
            #         "refClass", text=service["userclass"].name)
            #     number_of_visits.add_child(refclass)
            #     integer_visits = number_of_visits.add_child(
            #         _XmlNode("subParameter", attributes={
            #             "classPath": "java.lang.Integer",
            #             "name": "numberOfVisits"}))
            #     integer_visits.add_child(
            #         _XmlNode("value", text="1"))  # sempre uguale? boh
            for userclass in model.userclasses:
                refclass = _XmlNode(
                    "refClass", text=userclass.name)
                number_of_visits.add_child(refclass)
                integer_visits = number_of_visits.add_child(
                    _XmlNode("subParameter", attributes={
                        "classPath": "java.lang.Integer",
                        "name": "numberOfVisits"}))
                integer_visits.add_child(
                    _XmlNode("value", text="1"))  # sempre uguale? boh

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

            # Logger
            logger_node = baked_model.add_child(
                _XmlNode("node", attributes={"name": f"LOG_{node.name}"}))
            queue_section = logger_node.add_child(
                _XmlNode("section", attributes={"className": "Queue"}))
            size = queue_section.add_child(_XmlNode("parameter", attributes={
                "classPath": "java.lang.Integer", "name": "size"}))
            size.add_child(_XmlNode("value", text=-1))
            drop_strategy = queue_section.add_child(_XmlNode("parameter", attributes={
                "array": "true",
                "classPath": "java.lang.String",
                "name": "dropStrategies"
            }))
            queue_section.add_child(  # get queue strategy
                _XmlNode("parameter",
                         attributes={
                             "classPath": "jmt.engine.NetStrategies.QueueGetStrategies.FCFSstrategy",
                             "name": "FCFSstrategy"}))
            put_queue_strategy = queue_section.add_child(
                _XmlNode("parameter",
                         attributes={
                             "array": "true",
                             "classPath": "jmt.engine.NetStrategies.QueuePutStrategy",
                             "name": "QueuePutStrategy"}))
            for userclass in model.userclasses:
                drop_strategy.add_child(
                    _XmlNode("refClass", text=userclass.name))
                sub_par = drop_strategy.add_child(
                    _XmlNode("subParameter",
                             attributes={"classPath": "java.lang.String",
                                         "name": "dropStrategy"}))
                sub_par.add_child(
                    _XmlNode("value", text="BAS blocking"))

                # QUEUE STRATEGY
                put_queue_strategy.add_child(
                    _XmlNode("refClass", text=userclass.name))
                put_queue_strategy.add_child(
                    _XmlNode("subParameter",
                             attributes={
                                 "classPath": "jmt.engine.NetStrategies.QueuePutStrategies.TailStrategy",
                                 "name": "TailStrategy"}))

            logtunnel_section = logger_node.add_child(
                _XmlNode("section", attributes={"className": "LogTunnel"}))
            logtunnel_section.add_child(_XmlNode("parameter", children=[_XmlNode("value", text="global.csv")], attributes={
                "classPath": "java.lang.String",
                "name": "logfileName"
            }))
            logtunnel_section.add_child(_XmlNode("parameter", children=[_XmlNode("value", text=baked_model.path_folder)], attributes={
                "classPath": "java.lang.String",
                "name": "logfilePath"
            }))
            for bool_param in ["logExecTimestamp", "logLoggerName", "logTimeStamp", "logJobID", "logJobClass", "logTimeSameClass", "logTimeAnyClass"]:
                logtunnel_section.add_child(_XmlNode("parameter", children=[_XmlNode("value", text="true")], attributes={
                    "classPath": "java.lang.Boolean",
                    "name": bool_param
                }))
            logtunnel_section.add_child(_XmlNode("parameter", children=[_XmlNode("value", text=len(model.userclasses))], attributes={
                "classPath": "java.lang.Integer",
                "name": "numClasses"
            }))

            router_section = logger_node.add_child(
                _XmlNode("section", attributes={"className": "Router"}))
            routing_strategy = router_section.add_child(_XmlNode("parameter", attributes={
                "array": "true",
                "classPath": "jmt.engine.NetStrategies.RoutingStrategy",
                "name": "RoutingStrategy"
            }))
            for userclass in model.userclasses:
                routing_strategy.add_child(
                    _XmlNode("refClass", text=userclass.name))
                routing_strategy.add_child(_XmlNode("subParameter", attributes={
                    "classPath": "jmt.engine.NetStrategies.RoutingStrategies.RandomStrategy",
                    "name": "Random"
                }))

            # Router
            router = node_E.get_child(2)
            # da togliere node_index, si trova
            set_router(model, router, node_index)

    # ADD MEASURES qui sample

    baked_model.add_child(_XmlNode("measure", attributes={
        "alpha": "0.01",
        "name": "System Throughput",
        "nodeType": "",
        "precision": "0.03",
        "referenceNode": "",
        "referenceUserClass": "",
        "type": "System Throughput",
        "verbose": "false"
    }))

    # Add Connections
    # model.connections = []
    for matrix in model.matrices:
        for source, row in enumerate(matrix):
            for target, probability in enumerate(row):
                if probability > 0:
                    if not fill_loggers:
                        model.connections.append(
                            (model.nodes[source].name, model.nodes[target].name))
                    else:
                        model.connections.append(
                            (model.nodes[source].name, "LOG_"+model.nodes[target].name))
                        model.connections.append(
                            ("LOG_"+model.nodes[target].name, model.nodes[target].name))

    # Qui questione logger

    for connection in set(model.connections):
        baked_model.add_child(_XmlNode("connection", attributes={
            "source": connection[0],
            "target": connection[1]}))

    stations_to_be_blocked = [node for node in model.nodes if (
        isinstance(node, Station) and node.buffer_size > 0)]
    for node in stations_to_be_blocked:
        blocking_region = baked_model.add_child(_XmlNode("blockingRegion", attributes={
            "name": f"{node.name}_BLOCK",
            "type": "default"
        }))
        blocking_region.add_child(
            _XmlNode("regionNode", attributes={"nodeName": node.name}))
        blocking_region.add_child(_XmlNode("regionNode", attributes={
                                  "nodeName": f"LOG_{node.name}"}))
        blocking_region.add_child(
            _XmlNode("globalConstraint", attributes={"maxJobs": str(node.buffer_size)}))
        blocking_region.add_child(
            _XmlNode("globalMemoryConstraint", attributes={"maxMemory": str(-1)}))
        for userclass in model.userclasses:
            blocking_region.add_child(_XmlNode("classConstraint", attributes={
                "jobClass": userclass.name,
                "maxJobsPerClass": str(-1)
            }))
        for userclass in model.userclasses:
            blocking_region.add_child(_XmlNode("classMemoryConstraint", attributes={
                "jobClass": userclass.name,
                "maxMemoryPerClass": str(-1)
            }))
        for userclass in model.userclasses:
            blocking_region.add_child(_XmlNode("dropRules", attributes={
                "dropThisClass": "false",
                "jobClass": userclass.name
            }))
        for userclass in model.userclasses:
            blocking_region.add_child(_XmlNode("classWeight", attributes={
                "jobClass": userclass.name,
                "weight": str(1)
            }))
        for userclass in model.userclasses:
            blocking_region.add_child(_XmlNode("classSize", attributes={
                "jobClass": userclass.name,
                "size": str(1)  # CHE è??
            }))
    return baked_model


def add_userclass_elements(model, baked_model):
    for userclass in model.userclasses:
        if isinstance(userclass, OpenClass):
            baked_model.add_child(_OpenClass(
                baked_model, userclass.name, userclass.reference_station.name,
                userclass.distribution, userclass.priority))
        elif isinstance(userclass, ClosedClass):
            baked_model.add_child(_ClosedClass(
                baked_model, userclass.name, userclass.customers,
                userclass.reference_station.name, userclass.priority))


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
                    "classPath": "jmt.engine.NetStrategies.RoutingStrategies.EmpiricalStrategy",
                    "name": "Probabilities"}))
            empirical_entry_array = probabilities.add_child(
                _XmlNode("subParameter", attributes={
                    "array": "true",
                    "classPath": "jmt.engine.random.EmpiricalEntry",
                    "name": "EmpiricalEntryArray"}))
            empirical_entry = empirical_entry_array.add_child(
                _XmlNode("subParameter", attributes={
                    "classPath": "jmt.engine.random.EmpiricalEntry",
                    "name": "EmpiricalEntry"}))
            for target in targets:  # aggiungi esclusione connections
                empirical_entry.add_child(
                    _XmlNode("subParameter", attributes={
                        "classPath": "java.lang.String",
                        "name": "stationName"},
                        children=[_XmlNode("value", text=f"LOG_{model.nodes[target[0]].name}")]))
                empirical_entry.add_child(
                    _XmlNode("subParameter", attributes={
                        "classPath": "java.lang.Double",
                        "name": "probability"},
                        children=[_XmlNode("value", text=float(target[1]))]))
        else:
            pass
