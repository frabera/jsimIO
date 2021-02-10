# %%
import os
import subprocess
from datetime import datetime

from lxml import etree as ET

from .defaults import *
from .xmlnode_superclass import *


def write_jsimg(sim_element):
    now = datetime.now().strftime("%Y%m%d-%H%M%S")
    cwd = os.getcwd()
    modelname = sim_element.attrib["name"]
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


def solve_jsimg(path):
    ret = subprocess.run(
        [
            "java", "-cp", "JMT.jar", "jmt.commandline.Jmt", "sim", path,
            # "--illegal-access=permit"
        ], capture_output=True)

    if ret.stderr.startswith(b"[Error]"):
        print(ret.stderr.decode())

# %%

# %%
