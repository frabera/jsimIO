from .defaults import *
from .sections import (_Fork, _JobSink, _LogTunnel, _Queue, _RandomSource,
                       _Router, _Server, _ServiceTunnel, _Delay, _Join)
from .strategies import (DropStrategy, QueuePutStrategy, RoutingStrategy,
                         SchedStrategy)
from .xmlnode_superclass import _XmlNode, _SubParameter
from .distributions import Disable


class _Node(_XmlNode):
    def __init__(self, model, name):
        super().__init__("node", attributes={"name": name})
        self.model = model
        self.name = name
        self.classes_referenced = []
        self.routes = []

    def add_to_model(self):
        self.model.add_child(self)

    def add_route(self, userclass, target, probability):
        self.routes.append({
            "userclass": userclass,
            "target": target,
            "probability": probability
        })

    def create_pre_logger(self):
        if isinstance(self, Source):
            return
        logger = Logger(self.model, f"LOG_{self.name}")
        self.model.add_child(logger)
        self.model.connections.append(
            {"source": f"LOG_{self.name}", "target": self.name})

    def fill_data(self):  # Method to overwrite (custom) for each node
        pass

    def _set_routing_to(self, userclass, target, routing_strategy, probability):
        if isinstance(self, Station):
            self.router.add_routingstrategy_entry(userclass,
                                                  target,
                                                  routing_strategy,
                                                  probability)


class Station(_Node):  # manca maxjobs
    def __init__(self, model, name,
                 scheduling_strategy=SchedStrategy.FCFS, buffer_size=-1,
                 max_jobs=1, drop_strategy=DropStrategy.BAS_Blocking):
        super().__init__(model, name)
        self.scheduling_strategy = scheduling_strategy
        self.buffer_size = buffer_size
        self.drop_strategy = drop_strategy
        self.max_jobs = max_jobs
        # self.service_strategy = None
        # self.routing_strategy = None

        self.service = []

        self.queue = self.add_child(
            _Queue(scheduling_strategy, buffer_size, drop_strategy))
        self.server = self.add_child(_Server(self.max_jobs))
        self.router = self.add_child(_Router(self.model))

        self.model.nodes.append(self)

    def set_service(self, userclass, distribution):
        self.service.append(
            {"userclass": userclass, "distribution": distribution})

    def fill_data(self):
        # Service
        userclasses_not_served = [userclass
                                  for userclass in self.model.userclasses]
        for service in self.service:
            self.server.add_servicestrategy_entry(
                service["userclass"],
                service["distribution"]
            )
            userclasses_not_served.remove(service["userclass"])
        for not_served in userclasses_not_served:
            self.server.add_servicestrategy_entry(
                not_served,
                Disable()
            )
        # Number of visits
        for userclass in self.model.userclasses:
            self.server.add_numberofvisits_entry(userclass)
            # drop strategies
            self.queue.add_dropstrategy_entry(userclass, self.drop_strategy)
            # ! Tailstrategy HARDCODED!
            self.queue.add_queueput_entry(
                userclass, QueuePutStrategy.TailStrategy)


class Source(_Node):
    def __init__(self, model, name):
        super().__init__(model, name)

        self.model.nodes.append(self)

        self.random_source = self.add_child(_RandomSource())
        self.service_tunnel = self.add_child(_ServiceTunnel())
        self.router = self.add_child(_Router(self.model))


class Sink(_Node):
    def __init__(self, model, name):
        super().__init__(model, name)
        self.add_child(_JobSink())

        self.model.nodes.append(self)


class Fork(_Node):
    def __init__(self, model, name, forked_class_NameString,
                 scheduling_strategy=SchedStrategy.FCFS, buffer_size=-1,
                 drop_strategy=DropStrategy.BAS_Blocking):
        super().__init__(model, name)
        self.scheduling_strategy = scheduling_strategy
        self.buffer_size = buffer_size
        self.drop_strategy = drop_strategy
        self.forked_class = None
        self.forked_class_NameString = forked_class_NameString
        self.fork_subcomponents = []
        # self.service_strategy = None
        # self.routing_strategy = None
        self.model.nodes.append(self)

    def fill_data(self):
        self.forked_class = [
            userclass for userclass in self.model.userclasses if userclass.name == self.forked_class_NameString][0]
        self.queue = self.add_child(
            _Queue(self.scheduling_strategy, self.buffer_size, self.drop_strategy))
        self.service_tunnel = self.add_child(_ServiceTunnel())
        self.fork = self.add_child(
            _Fork(self.forked_class))

        # Number of visits
        for userclass in self.model.userclasses:
            # drop strategies
            self.queue.add_dropstrategy_entry(userclass, self.drop_strategy)
            # ! Tailstrategy HARDCODED!
            self.queue.add_queueput_entry(
                userclass, QueuePutStrategy.TailStrategy)

    def fill_fork(self, connections, matrices):
        outpaths_id = []
        this_fork_id = self.model.nodes.index(self)

        for connection in connections:
            node_names = [node.name for node in self.model.nodes]
            source_id = node_names.index(connection["source"])
            target_id = node_names.index(connection["target"][4:])
            if source_id == this_fork_id:
                outpaths_id.append(target_id)

        for userclass_id, userclass in enumerate(self.model.userclasses):
            if userclass is not self.forked_class:
                branch_probabilities = self.fork.fork_strategy.add_subparameter_siblings(
                    "jmt.engine.NetStrategies.ForkStrategies.ProbabilitiesFork",
                    "Branch Probabilities", userclass.name)
                outpath_array = branch_probabilities.add_child(_SubParameter(
                    "jmt.engine.NetStrategies.ForkStrategies.OutPath",
                    "EmpiricalEntryArray", array="true"))

                for outpath in outpaths_id:
                    outpath_entry = outpath_array.add_child(_SubParameter(
                        "jmt.engine.NetStrategies.ForkStrategies.OutPath",
                        "OutPathEntry"))
                    out_unit_probability = outpath_entry.add_child(_SubParameter(
                        "jmt.engine.random.EmpiricalEntry",
                        "outUnitProbability"))
                    out_unit_probability.add_child(_SubParameter(
                        "java.lang.String",
                        "stationName",
                        value=f"LOG_{self.model.nodes[outpath].name}"))
                    out_unit_probability.add_child(_SubParameter(
                        "java.lang.Double",
                        "probability",
                        # value=str(float(matrices[userclass_id][outpath][target_id]))))  # ! MUST BE 1.0?
                        value="0.0"))

                    jobs_per_link = outpath_entry.add_child(_SubParameter(
                        "jmt.engine.random.EmpiricalEntry",
                        "JobsPerLinkDis",
                        array="true"))
                    jobs_entry = jobs_per_link.add_child(_SubParameter(
                        "jmt.engine.random.EmpiricalEntry",
                        "EmpiricalEntry"))
                    jobs_entry.add_child(_SubParameter(
                        "java.lang.String",
                        "numbers",
                        # value=str(1)))  # ! HARDCODED
                        value="1"))
                    jobs_entry.add_child(_SubParameter(
                        "java.lang.Double",
                        "probability",
                        # value=str(float(matrices[userclass_id][this_fork_id][target_id]))))  # ! HARDCODED
                        value="1.0"))

            else:  # Multi branch class-switch
                multi_branch = self.fork.fork_strategy.add_subparameter_siblings(
                    "jmt.engine.NetStrategies.ForkStrategies.MultiBranchClassSwitchFork", "Multi-Branch Class Switch", userclass.name)
                classjob_array = multi_branch.add_child(_SubParameter(
                    "jmt.engine.NetStrategies.ForkStrategies.ClassJobNum",
                    "ClassJobNumArray",
                    array="true"))
                for outpath in outpaths_id:
                    outpath_entry = classjob_array.add_child(_SubParameter(
                        "jmt.engine.NetStrategies.ForkStrategies.ClassJobNum",
                        "OutPathEntry"))
                    station_name = outpath_entry.add_child(_SubParameter(
                        "java.lang.String",
                        "stationName",
                        value=f"LOG_{self.model.nodes[outpath].name}"))
                    classes = outpath_entry.add_child(_SubParameter(
                        "java.lang.String",
                        "Classes",
                        array="true"))
                    numbers = outpath_entry.add_child(_SubParameter(
                        "java.lang.String",
                        "Numbers",
                        array="true"))
                    for userclass_id, userclass in enumerate(self.model.userclasses):
                        classes.add_child(_SubParameter("java.lang.String",
                                                        "class",
                                                        value=userclass.name))

                        if matrices[userclass_id][this_fork_id][outpath] > 0.0001:
                            jobs_number_value = str(1)
                        else:
                            jobs_number_value = str(0)
                        numbers.add_child(_SubParameter(
                            "java.lang.String",
                            "numberOfJobs",
                            value=jobs_number_value))


class Join(_Node):
    def __init__(self, model, name, output, number_of_class_inputs):
        super().__init__(model, name)

        self.join = self.add_child(
            _Join(model.userclasses, output, number_of_class_inputs))
        self.service_tunnel = self.add_child(_ServiceTunnel())
        self.router = self.add_child(_Router(self.model))

        self.model.nodes.append(self)


class Delay(_Node):
    def __init__(self, model, name):
        super().__init__(model, name)
        self.buffer_size = -1

        # self.service_strategy = None
        # self.routing_strategy = None

        self.service = []

        self.queue = self.add_child(
            _Queue(SchedStrategy.FCFS, self.buffer_size,
                   DropStrategy.BAS_Blocking))  # ! originariamente è DROP
        self.server = self.add_child(_Delay())
        self.router = self.add_child(_Router(self.model))

        self.model.nodes.append(self)

    def set_service(self, userclass, distribution):
        self.service.append(
            {"userclass": userclass, "distribution": distribution})

    def fill_data(self):
        # Service
        userclasses_not_served = [userclass
                                  for userclass in self.model.userclasses]
        for service in self.service:
            self.server.add_servicestrategy_entry(
                service["userclass"],
                service["distribution"]
            )
            userclasses_not_served.remove(service["userclass"])
        for not_served in userclasses_not_served:
            self.server.add_servicestrategy_entry(
                not_served,
                Disable()
            )
        # Number of visits
        for userclass in self.model.userclasses:
            self.queue.add_dropstrategy_entry(
                userclass, DropStrategy.BAS_Blocking)
            # ! Tailstrategy HARDCODED!
            self.queue.add_queueput_entry(
                userclass, QueuePutStrategy.TailStrategy)


class Logger(_Node):
    def __init__(self, model, name):
        super().__init__(model, name)
        self._queue = self.add_child(
            _Queue(SchedStrategy.FCFS, -1, DropStrategy.BAS_Blocking))

        # self.model.nodes.append(self)
        # DA RIVEDERE I PARAMETRI
        #  ! verificare che array sia true anche se una sola classe
        #  ! verificare se devo inserire solo le classi che passano
        #  ! dalla stazione o le posso mettere tutte

        for userclass in model.userclasses:
            # L'userclass passa dalla stazione
            # if sum(model.matrices[uc_index][node_index]) > 0:
            self._queue.add_dropstrategy_entry(
                userclass, DropStrategy.BAS_Blocking)
            self._queue.add_queueput_entry(
                userclass, QueuePutStrategy.TailStrategy)
        addition_dict = {
            "classPath": "java.lang.Integer",
            "name": "numClasses",
            "value": len(self.model.userclasses)
        }
        sum_options = Default.LoggerOptions.copy()
        sum_options.append(addition_dict)
        self.log_tunnel = self.add_child(
            _LogTunnel(sum_options, modelname=self.model.name))

        self.router = self.add_child(
            _Router(model, routing_strategy=RoutingStrategy.Random))
