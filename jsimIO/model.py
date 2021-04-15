# from .nodes import _Node
from jsimIO.strategies import RoutingStrategy
import os
import subprocess
from datetime import datetime

from lxml import etree as ET

from .defaults import *
from .xmlnode_superclass import _XmlNode
from .nodes import Sink, Station, Fork
from .measures import Measure


class Model(_XmlNode):
    def __init__(self, name, options=Default.ModelOptions):
        self.name = name
        self.options = options
        self.userclasses = []
        self.nodes = []
        self.connections = []
        self.matrices = None
        self.measures = []

        # Element XML
        super().__init__("sim")
        self.set_attributes({**{"name": self.name}, **self.options})

        # SCRITTURA
        now = datetime.now().strftime("%Y%m%d-%H%M%S")
        cwd = os.getcwd()
        folder = name+"_"+now
        self.path_folder = os.path.join(cwd, folder)
        try:
            os.mkdir(self.path_folder)
        except OSError:
            print(f"Creation of the directory {folder} failed")
        self.filename = name + "-input.jsimg"
        self.filepath = os.path.join(self.path_folder, self.filename)

    # TBD
    def add_measure(self, measure=Measure.SystemThroughput, station=None,
                    options=Default.MeasureOptions):
        self.measures.append(_XmlNode("measure", attributes={
            "alpha": "0.01",
            "name": "System Throughput",
            "nodeType": "",
            "precision": "0.03",
            "referenceNode": "",
            "referenceUserClass": "",
            "type": "System Throughput",
            "verbose": "false"}))

    def set_routing_matrices(self, matrices):
        self.matrices = matrices

    def write_jsimg(self):
        for node in self.nodes:
            node.fill_data()

            node.add_to_model()
        self._set_routing()  # !
        for node_index, node in enumerate(self.nodes):
            if isinstance(node, Fork):
                node.fill_fork(self.connections, self.matrices)

        for node in self.nodes:
            node.create_pre_logger()

        for measure in self.measures:
            self.add_child(measure)
        for connection in self.connections:
            self.add_child(_XmlNode("connection", attributes=connection))
        stations_to_be_blocked = [node for node in self.nodes if (
            isinstance(node, Station) and node.buffer_size > 0)]
        for node in stations_to_be_blocked:
            blocking_region = self.add_child(_XmlNode("blockingRegion", attributes={
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
            for userclass in self.userclasses:
                blocking_region.add_child(_XmlNode("classConstraint", attributes={
                    "jobClass": userclass.name,
                    "maxJobsPerClass": str(-1)
                }))
            for userclass in self.userclasses:
                blocking_region.add_child(_XmlNode("classMemoryConstraint", attributes={
                    "jobClass": userclass.name,
                    "maxMemoryPerClass": str(-1)
                }))
            for userclass in self.userclasses:
                blocking_region.add_child(_XmlNode("dropRules", attributes={
                    "dropThisClass": "false",
                    "jobClass": userclass.name
                }))
            for userclass in self.userclasses:
                blocking_region.add_child(_XmlNode("classWeight", attributes={
                    "jobClass": userclass.name,
                    "weight": str(1)
                }))
            for userclass in self.userclasses:
                blocking_region.add_child(_XmlNode("classSize", attributes={
                    "jobClass": userclass.name,
                    "size": str(1)  # CHE è??
                }))
        sim_element = self._element
        NSMAP = {"xsi": "http://www.w3.org/2001/XMLSchema-instance"}
        archive = ET.Element("archive", nsmap=NSMAP)  # * archive
        archive.attrib["name"] = self.filename
        attr_qname = ET.QName(
            "http://www.w3.org/2001/XMLSchema-instance", "noNamespaceSchemaLocation")
        archive.attrib[attr_qname] = "Archive.xsd"

        archive.append(sim_element)  # * sim
        sim_element.attrib[attr_qname] = "SIMmodeldefinition.xsd"
        sim_element.attrib["logPath"] = self.path_folder
        tree = ET.ElementTree(archive)
        # ET.indent(tree, space="    ")  # * ETree, non va
        tree.write(self.filepath, xml_declaration=True, encoding="ISO-8859-1",
                   standalone=False, pretty_print=True)
        return self.filepath  # Non necessario

    def solve_jsimg(self, path=None, max_memory_mb=-1, seed=None):
        if not path:
            path = self.filepath
        if max_memory_mb == -1:
            ret = subprocess.run(
                [
                    "java",
                    "-cp", r"jsimIO\JMT.jar",
                    "jmt.commandline.Jmt", "sim", path,
                    "-seed" if seed else "",
                    str(seed) if seed else ""
                    # "--illegal-access=permit"
                ], capture_output=True)
        else:
            ret = subprocess.run(
                [
                    "java",
                    f"-Xmx{max_memory_mb}m",
                    "-cp", r"jsimIO\JMT.jar",
                    "jmt.commandline.Jmt", "sim", path,
                    "-seed" if seed else "",
                    str(seed) if seed else ""
                    # "--illegal-access=permit"
                ], capture_output=True)

        if ret.stderr.startswith(b"[Error]"):
            print(ret.stderr.decode())
        return ret

    def _set_routing(self, matrices=None):
        if self.matrices is None:
            num_nodes = len(self.nodes)
            num_classes = len(self.userclasses)
            self.matrices = [
                [
                    [0 for _ in range(num_nodes)]
                    for _ in range(num_nodes)
                ]
                for _ in range(num_classes)
            ]  # Creates a n_userclasses*n_nodes*n_nodes dimensional matrix
            # (a list with one square matrix of dimension n_nodes for each userclass)

            for node in [node for node in self.nodes if not isinstance(node, Sink)]:
                for route in node.routes:
                    id_userclass = self.userclasses.index(route["userclass"])
                    id_source_node = self.nodes.index(node)
                    id_target_node = self.nodes.index(route["target"])
                    self.matrices[id_userclass][id_source_node][id_target_node] = route["probability"]
        assert len(self.matrices) == len(self.userclasses), \
            "The number of matrices must be equal to the number of customer classes"
        #  normalizzare

        def normalize(row):
            row_sum = sum(row)
            return [i/row_sum for i in row]
        for matrix in self.matrices:
            for row in matrix:
                if sum(row) > 0:
                    row = normalize(row)
        # for userclass_index, matrix in enumerate(self.matrices):
        #     for node_index, node in enumerate(self.nodes):
        #         if isinstance(node, Fork):
        #             # STUFF
        #             continue

        #         if sum(matrix[node_index]) > 0:
        #             targets = [(index, prob) for index, prob in enumerate(
        #                 matrix[node_index]) if prob > 0.000000000001]  # ! no Così metto anche le probabilità nulle
        #             for target, probability in targets:
        #                 if (self.nodes[node_index].name, f"LOG_{self.nodes[target].name}") not in [(d["source"], d["target"]) for d in self.connections]:
        #                     self.connections.append(
        #                         {"source": self.nodes[node_index].name, "target": f"LOG_{self.nodes[target].name}"})
        #                 # node._set_routing_to(self.userclasses[userclass_index],
        #                 #                      self.nodes[target],
        #                 #                      RoutingStrategy.Probabilities,
        #                 #                      probability)
        #                 node.router.add_routingstrategy_entry(self.userclasses[userclass_index],
        #                                                       self.nodes[target],
        #                                                       RoutingStrategy.Probabilities,
        #                                                       probability)

        self.route_dict = {}
        for node in self.nodes:
            self.route_dict[node] = []
        for userclass_index, matrix in enumerate(self.matrices):
            for node_index, node in enumerate(self.nodes):

                if sum(matrix[node_index]) > 0:
                    targets = [(index, prob) for index, prob in enumerate(
                        matrix[node_index]) if prob > 0.0000000001]
                    for target, probability in targets:
                        if (self.nodes[node_index].name, f"LOG_{self.nodes[target].name}") not in \
                                [(d["source"], d["target"]) for d in self.connections]:
                            self.connections.append(
                                {
                                    "source": self.nodes[node_index].name,
                                    "target": f"LOG_{self.nodes[target].name}"
                                })

            for connection in self.connections:
                node_names = [
                    node.name for node in self.nodes]
                source_id = node_names.index(connection["source"])
                target_id = node_names.index(connection["target"][4:])
                if not isinstance(self.nodes[source_id], Fork):
                    if not isinstance(self.nodes[source_id], Sink):
                        self.route_dict[self.nodes[source_id]].append({
                            "userclass": self.userclasses[userclass_index],
                            "target": self.nodes[target_id],
                            "routing_strategy": RoutingStrategy.Probabilities,
                            "probability": matrix[source_id][target_id]
                        })
                    # self.nodes[source_id].router.add_routingstrategy_entry(
                    #     self.userclasses[userclass_index],
                    #     self.nodes[target_id],
                    #     RoutingStrategy.Probabilities,
                    #     matrix[source_id][target_id])
        for node in self.route_dict.keys():
            if not isinstance(node, Sink):
                if not isinstance(node, Fork):
                    node.router.add_routingstrategy_entry(
                        self.route_dict[node])
