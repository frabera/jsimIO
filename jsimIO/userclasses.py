from .xmlnode_superclass import _XmlNode
import lxml.etree as ET
from .defaults import *


class _UserClass(_XmlNode):
    def __init__(self, model, name, type, reference_station, priority):
        super().__init__("userClass")
        self.name = name
        self.type = type
        self.reference_station = reference_station
        self.priority = priority
        model.add_child(self)

        # POST
        attribute_dict = self.get_classattributes_asdict()
        attribute_dict.pop("distribution", None)
        attribute_dict.pop("reference_station")
        attribute_dict.update({"referenceStation": reference_station.name})
        self.set_attributes(attribute_dict)


class ClosedClass(_UserClass):  # da distribuire i parametri
    def __init__(self, model, name, customers, reference_station, priority=0):
        self.customers = customers
        super().__init__(model, name, "closed", reference_station, priority)
        random_source = reference_station.get_child(Id.Source.RandomSource)
        # Parameter -> Subparameters
        parameter = _XmlNode("parameter", attributes={
                             "array": "true", "classPath": "jmt.engine.NetStrategies.ServiceStrategy", "name": "ServiceStrategy"})
        refclass = _XmlNode("refClass", text=self.name)
        parameter.add_child(refclass)
        subParameter = _XmlNode("subParameter", attributes={
                                "classPath": "jmt.engine.NetStrategies.ServiceStrategies.ServiceTimeStrategy", "name": "ServiceTimeStrategy"})
        subParameter.add_child(_XmlNode("value", text="null"))
        parameter.add_child(subParameter)
        # Problema: parameter potrebbe già esistere, in tal caso devo aggiungere solo refclass e subpar
        # assunto che sia solo 1
        # if random_source._element.find("parameter"):
        #     random_source._element.find("parameter").append(
        #         refclass._element)  # Stesso problema di giù
        #     random_source._element.find("parameter").append(
        #         subParameter._element)  # Stesso problema di giù
        # else:
        #     random_source.add_child(parameter)

        # Qui assumo che ci possa essere un solo parametro
        if random_source._element.find("parameter"):
            random_source.get_child(0).add_child(refclass)
            random_source.get_child(0).add_child(subParameter)
        else:
            random_source.add_child(parameter)
            # idem giù da fare


class OpenClass(_UserClass):
    def __init__(self, model, name, reference_station, distribution, priority=0):
        self.distribution = distribution
        super().__init__(model, name, "open", reference_station, priority)

        # Parameter -> Subparameters ! QUA USO SOLO ELEMENT INVECE CHE DICT!!!! CAMBIARE!
        random_source = reference_station.get_child(Id.Source.RandomSource)
        parameter = _XmlNode("parameter", attributes={
                             "array": "true", "classPath": "jmt.engine.NetStrategies.ServiceStrategy", "name": "ServiceStrategy"})
        refclass = _XmlNode("refClass", text=self.name)
        parameter.add_child(refclass)
        distribution_parameters_list = distribution.get_elements_list()
        for elem in distribution_parameters_list:
            # TODO cambiare dist in modo che ritorni dict e non list_xml
            parameter._element.append(elem)
        # Problema: parameter potrebbe già esistere, in tal caso devo aggiungere solo refclass e subpar
        # assunto che sia solo 1
        if random_source._element.find("parameter"):
            random_source._element.find("parameter").append(refclass._element)
            for elem in distribution_parameters_list:
                random_source._element.find("parameter").append(elem)
        else:
            # discrepanza tra parameter._children e parameter._element
            random_source.add_child(parameter)
