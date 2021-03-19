# from .nodes import _Node
import os
import subprocess
from datetime import datetime

from lxml import etree as ET

from .defaults import *
from .xmlnode_superclass import _XmlNode
# from .userclasses import _UserClass


class _Model(_XmlNode):
    def __init__(self, input_model, options=Default.ModelOptions):
        super().__init__("sim")

        self.name = input_model.name  # ci deve finire negli attributi per sim tag
        #  self.options = options O IN ALTERNATIVA:
        for key in options:
            setattr(self, key, options[key])
        self.set_attributes(self.get_classattributes_asdict())
        self.input_model = input_model

        # SCRITTURA
        now = datetime.now().strftime("%Y%m%d-%H%M%S")
        cwd = os.getcwd()
        modelname = self.name  # ! rinominato, verificare che sia tutto a posto
        folder = f"{modelname}_{now}"
        self.path_folder = os.path.join(cwd, folder)

        try:
            os.mkdir(self.path_folder)
        except OSError:
            print(f"Creation of the directory {folder} failed")
        self.filename = modelname + "-input.jsimg"
        self.filepath = os.path.join(self.path_folder, self.filename)

    def write_jsimg(self):
        sim_element = self._element
        # self.add_child(_XmlNode("measure", attributes={
        #     "alpha": "0.01",
        #     "name": "System Throughput",
        #     "nodeType": "",
        #     "precision": "0.03",
        #     "referenceNode": "",
        #     "referenceUserClass": "",
        #     "type": "System Throughput",
        #     "verbose": "false"
        # }))
        # now = datetime.now().strftime("%Y%m%d-%H%M%S")
        # cwd = os.getcwd()
        # modelname = self.name  # ! rinominato, verificare che sia tutto a posto
        # folder = f"{modelname}_{now}"
        # path_folder = os.path.join(cwd, folder)

        # try:
        #     os.mkdir(path_folder)
        # except OSError:
        #     print(f"Creation of the directory {folder} failed")
        # filename = modelname + "-input.jsimg"
        # filepath = os.path.join(path_folder, filename)

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
        ET.indent(tree, space="    ")  # * ETree
        tree.write(self.filepath, xml_declaration=True, encoding="ISO-8859-1",
                   standalone=False, pretty_print=True)
        return self.filepath

    def solve_jsimg(self, path):
        ret = subprocess.run(
            [
                "java", "-cp", r"jsimIO\JMT.jar", "jmt.commandline.Jmt", "sim", path
                # "--illegal-access=permit"
            ], capture_output=True)

        if ret.stderr.startswith(b"[Error]"):
            print(ret.stderr.decode())

        return ret
