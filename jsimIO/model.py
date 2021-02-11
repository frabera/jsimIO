from jsimIO.nodes import _Node
import os
import subprocess
from datetime import datetime

from lxml import etree as ET

from .defaults import *
from .xmlnode_superclass import _XmlNode


class Model(_XmlNode):
    def __init__(self, name, options=Default.ModelOptions):
        super().__init__("sim")
        self._name = name  # PRIVATO PERCHè SE NO MI FINISCE NEGLI ATTRIBUTI
        #  self.options = options O IN ALTERNATIVA:
        for key in options:
            setattr(self, key, options[key])
        self.set_attributes(self.get_classattributes_asdict())

    def get_nodes(self):
        return [child for child in self._children if isinstance(child, _Node)]

    def set_routing(self, matrices, fill_loggers=False):
        def normalize(matrix):
            for row in matrix:
                sum_row = sum(row)
                if sum_row:
                    for elem in row:
                        elem = elem/sum_row
            return matrix

        for matrix in matrices:
            normalize(matrix)

        # Add connections
        stations = [node for node in self._children if type(node) in [
            "jsimIO.nodes.Source"]]
        for matrix in matrices:
            for i in range(len(matrix)):
                for j in matrix[i]:
                    if matrix[i][j] is not 0:
                        source = self.get_nodes()[i].name
                        target = self.get_nodes()[j].name
                        self.add_child(_XmlNode("connection", attributes={
                                       "source": source, "target": target}))

        # Add routing
    # def write_jsimg(self, sim_element):

    def write_jsimg(self):
        sim_element = self._element
        now = datetime.now().strftime("%Y%m%d-%H%M%S")
        cwd = os.getcwd()
        modelname = self._name
        folder = f"{modelname}_{now}"
        path_folder = os.path.join(cwd, folder)

        try:
            os.mkdir(path_folder)
        except OSError:
            print(f"Creation of the directory {folder} failed")
        filename = modelname + "-input.jsimg"
        filepath = os.path.join(path_folder, filename)

        NSMAP = {"xsi": "http://www.w3.org/2001/XMLSchema-instance"}
        archive = ET.Element("archive", nsmap=NSMAP)  # * archive
        archive.attrib["name"] = filename
        attr_qname = ET.QName(
            "http://www.w3.org/2001/XMLSchema-instance", "noNamespaceSchemaLocation")
        archive.attrib[attr_qname] = "Archive.xsd"

        archive.append(sim_element)  # * sim
        sim_element.attrib[attr_qname] = "SIMmodeldefinition.xsd"

        tree = ET.ElementTree(archive)  # * ETree
        tree.write(filepath, xml_declaration=True, encoding="ISO-8859-1",
                   standalone=False, pretty_print=True)
        return filepath

    def solve_jsimg(self, path):
        ret = subprocess.run(
            [
                "java", "-cp", "JMT.jar", "jmt.commandline.Jmt", "sim", path,
                # "--illegal-access=permit"
            ], capture_output=True)

        if ret.stderr.startswith(b"[Error]"):
            print(ret.stderr.decode())
