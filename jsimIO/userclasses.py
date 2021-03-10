from .xmlnode_superclass import _XmlNode
# import lxml.etree as ET
from .defaults import *


class _UserClass(_XmlNode):
    def __init__(self, model, name, type, reference_station, priority):
        super().__init__("userClass")
        self.name = name
        self.reference_station = reference_station
        self.type = type
        self.priority = priority

        # addchildqui

        # POST
        attribute_dict = self.get_classattributes_asdict()
        attribute_dict.pop("distribution", None)
        attribute_dict.pop("reference_station")
        # attribute_dict.update({"referenceStation": reference_station})
        # ! Source o station? per openclass in source è source
        attribute_dict.update({"referenceSource": reference_station})
        self.set_attributes(attribute_dict)

        model.add_child(self)


class _ClosedClass(_UserClass):  # da distribuire i parametri
    def __init__(self, model, name, customers, reference_station, priority=0):
        self.customers = customers
        super().__init__(model, name, "closed", reference_station, priority)
        # Parameter -> Subparameters
        parameter = _XmlNode("parameter", attributes={
                             "array": "true", "classPath": "jmt.engine.NetStrategies.ServiceStrategy", "name": "ServiceStrategy"})
        refclass = _XmlNode("refClass", text=self.name)
        parameter.add_child(refclass)
        subParameter = _XmlNode("subParameter", attributes={
                                "classPath": "jmt.engine.NetStrategies.ServiceStrategies.ServiceTimeStrategy", "name": "ServiceTimeStrategy"})
        subParameter.add_child(_XmlNode("value", text="null"))
        parameter.add_child(subParameter)


class _OpenClass(_UserClass):
    def __init__(self, model, name, reference_station, distribution, priority=0):
        self.distribution = distribution
        super().__init__(model, name, "open", reference_station, priority)

        # Parameter -> Subparameters ! QUA USO SOLO ELEMENT INVECE CHE DICT!!!! CAMBIARE!
        parameter = _XmlNode("parameter", attributes={
                             "array": "true", "classPath": "jmt.engine.NetStrategies.ServiceStrategy", "name": "ServiceStrategy"})
        refclass = _XmlNode("refClass", text=self.name)
        parameter.add_child(refclass)
        distribution_parameters_list = distribution.get_elements_list()
        for elem in distribution_parameters_list:
            # TODO cambiare dist in modo che ritorni dict e non list_xml
            parameter._element.append(elem)
