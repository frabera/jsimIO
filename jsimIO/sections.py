from .xmlnode_superclass import *
from .xmlnode_superclass import _Parameter, _SubParameter, _XmlNode
from .strategies import *
from os import getcwd
from os.path import join


class _Section(_XmlNode):
    def __init__(self, className):
        super().__init__("section")
        self.set_attributes({"className": className})

    # Per randomsource e per server
    def add_servicestrategy_entry(self, userclass, distribution):
        self.par_service_strategy.add_child(
            _XmlNode("refClass", text=userclass.name))
        self.par_service_strategy.add_child(distribution)


class _Queue(_Section):  # is a section
    def __init__(self, scheduling_strategy, buffer_size, drop_strategy):
        super().__init__("Queue")
        self.scheduling_strategy = scheduling_strategy
        self.par_buffersize = self.add_child(
            _Parameter("java.lang.Integer", "size", value=buffer_size)
        )
        self.par_dropstrategy = self.add_child(
            _Parameter("java.lang.String", "dropStrategies", array="true")
        )

        self.par_queueget = self.add_child(
            scheduling_strategy._get_queueget_node()
        )
        self.par_queueput = self.add_child(
            _Parameter("jmt.engine.NetStrategies.QueuePutStrategy",
                       "QueuePutStrategy", array="true")
        )

    def add_dropstrategy_entry(self, userclass, drop_strategy):
        self.par_dropstrategy.add_subparameter_siblings(
            "java.lang.String", "dropStrategy", userclass.name, drop_strategy)

    def add_queueput_entry(self, userclass, queueput_strategy):
        self.par_queueput.add_subparameter_siblings(
            queueput_strategy["classPath"], queueput_strategy["name"], userclass.name)


class _Server(_Section):
    def __init__(self, max_jobs, service_strategy=None):
        super().__init__("Server")
        self.max_jobs = max_jobs
        self.service_strategy = service_strategy

        self.add_child(
            _Parameter("java.lang.Integer", "maxJobs", value=max_jobs)
        )

        self.par_number_of_visits = self.add_child(
            _Parameter("java.lang.Integer", "numberOfVisits", array="true")
        )
        self.par_service_strategy = self.add_child(
            _Parameter("jmt.engine.NetStrategies.ServiceStrategy",
                       "ServiceStrategy", array="true")
        )

    def add_numberofvisits_entry(self, userclass):
        self.par_number_of_visits.add_subparameter_siblings(
            "java.lang.Integer", "numberOfVisits", userclass.name, value=str(1))


class _Router(_Section):
    def __init__(self, model, routing_strategy=None):
        super().__init__("Router")
        self.routing_strategy = routing_strategy

        self.par_routingstrategy = self.add_child(
            _Parameter("jmt.engine.NetStrategies.RoutingStrategy",
                       "RoutingStrategy", array="true")
        )

        if self.routing_strategy == RoutingStrategy.Random:
            for userclass in model.userclasses:
                self.par_routingstrategy.add_subparameter_siblings(
                    routing_strategy["classPath"], routing_strategy["name"], userclass.name)

        self.ref_classes = []

    # def add_routingstrategy_entry(self, userclass, target, type, value):
    #     vector_check = [
    #         (node._tag, node._text) for node in self.par_routingstrategy._children]
    #     if ("refClass", userclass.name) in vector_check:
    #         index_ins = vector_check.index(("refClass", userclass.name))
    #         empirical_strategy = self.par_routingstrategy.insert_child(index_ins, _SubParameter(
    #             "jmt.engine.NetStrategies.RoutingStrategies.EmpiricalStrategy", "Probabilities"))
    #         print("CIAO")
    #     else:
    #         self.par_routingstrategy.add_child(
    #             _XmlNode("refClass", text=userclass.name))
    #         empirical_strategy = self.par_routingstrategy.add_child(_SubParameter(
    #             "jmt.engine.NetStrategies.RoutingStrategies.EmpiricalStrategy", "Probabilities"))
    #     empirical_array = empirical_strategy.add_child(_SubParameter(
    #         "jmt.engine.random.EmpiricalEntry", "EmpiricalEntryArray", array="true"))
    #     entry = empirical_array.add_child(_SubParameter(
    #         "jmt.engine.random.EmpiricalEntry", "EmpiricalEntry"))
    #     entry.add_child(_SubParameter("java.lang.String",
    #                                   "stationName", value=f"LOG_{target.name}"))  # ! CI HO MESSO LOG
    #     entry.add_child(_SubParameter("java.lang.Double",
    #                                   "probability", value=str(float(value))))

    def add_routingstrategy_entry(self, list_of_dicts):
        # "userclass", "target","routing_strategy", "probability"

        userclass_list = list(set([entry["userclass"]
                                   for entry in list_of_dicts]))

        for userclass in userclass_list:

            empirical_strategy = self.par_routingstrategy.add_subparameter_siblings(
                "jmt.engine.NetStrategies.RoutingStrategies.EmpiricalStrategy",
                "Probabilities", refClass=userclass.name
            )

            entry_array = empirical_strategy.add_child(_SubParameter(
                "jmt.engine.random.EmpiricalEntry",
                "EmpiricalEntryArray",
                array="true"
            ))
            target_list = list(set(
                [entry["target"] for entry in list_of_dicts if entry["userclass"] is userclass]))
            for target in target_list:
                entry = [entry for entry in list_of_dicts if (
                    entry["userclass"] is userclass and entry["target"] is target)][0]

                empirical_entry = entry_array.add_child(_SubParameter(
                    "jmt.engine.random.EmpiricalEntry",
                    "EmpiricalEntry"
                ))

                empirical_entry.add_child(_SubParameter(
                    "java.lang.String",
                    "stationName",
                    value=f"LOG_{entry['target'].name}"
                ))
                empirical_entry.add_child(_SubParameter(
                    "java.lang.Double",
                    "probability",
                    value=str(float(entry["probability"]))
                ))


class _RandomSource(_Section):
    def __init__(self):
        super().__init__("RandomSource")
        self.par_service_strategy = self.add_child(
            _Parameter("jmt.engine.NetStrategies.ServiceStrategy",
                       "ServiceStrategy", array="true")
        )


class _ServiceTunnel(_Section):
    def __init__(self):
        super().__init__("ServiceTunnel")


class _LogTunnel(_Section):
    def __init__(self, options, modelname):
        super().__init__("LogTunnel")
        # Imposto la cartella nomemodello
        for option in options:
            if option["name"] == "logfilePath":
                option["value"] = join(getcwd(), modelname)
            self.add_child(
                _Parameter(option["classPath"],
                           option["name"], value=option["value"])
            )


class _JobSink(_Section):
    def __init__(self):
        super().__init__("JobSink")


class _Fork(_Section):
    def __init__(self, forked_class):
        super().__init__("Fork")
        self.add_child(_Parameter("java.lang.Integer",
                                  "jobsPerLink", value=str(1)))
        self.add_child(_Parameter("java.lang.Integer", "block", value=str(-1)))
        self.add_child(_Parameter("java.lang.Boolean",
                                  "isSimplifiedFork", value="false"))
        self.fork_strategy = self.add_child(_Parameter(
            "jmt.engine.NetStrategies.ForkStrategy", "ForkStrategy", array="true"))


class _Join(_Section):
    # TODO deduce the n_inputs from routing
    def __init__(self, model_userclasses, output_class, number_of_class_inputs):
        super().__init__("Join")
        self.join_strategy = self.add_child(
            _Parameter("jmt.engine.NetStrategies.JoinStrategy",
                       "JoinStrategy", array="true"))

        for component in [userclass for userclass in model_userclasses if userclass is not output_class]:
            standard_join = self.join_strategy.add_subparameter_siblings(
                "jmt.engine.NetStrategies.JoinStrategies.NormalJoin",
                "Standard Join", component.name)
            standard_join.add_child(_SubParameter(
                "java.lang.Integer", "numRequired", value=-1))

        quorum = self.join_strategy.add_subparameter_siblings(
            "jmt.engine.NetStrategies.JoinStrategies.PartialJoin", "Quorum", output_class.name)
        quorum.add_child(_SubParameter("java.lang.Integer",
                                       "numRequired", value=number_of_class_inputs))


class _Delay(_Section):
    def __init__(self):
        super().__init__("Delay")
        self.max_jobs = 1

        self.par_service_strategy = self.add_child(
            _Parameter("jmt.engine.NetStrategies.ServiceStrategy",
                       "ServiceStrategy", array="true")
        )
