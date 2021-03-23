from .xmlnode_superclass import _XmlNode
from .nodes import Fork, Source


class _UserClass(_XmlNode):
    def __init__(self, model, name, type, reference_station, priority):
        super().__init__("userClass")
        self.model = model
        self.name = name
        self.reference_station = reference_station
        self.type = type
        self.priority = priority

        if isinstance(reference_station, Fork):
            reference_station.fork_subcomponents.append(self)

        attribute_dict = self.get_classattributes_asdict()
        attribute_dict.pop("distribution", None)
        attribute_dict.pop("reference_station")
        self.set_attributes(attribute_dict)
        # reference source missing
        model.add_child(self)


class OpenClass(_UserClass):
    def __init__(self, model, name, reference_station, distribution=None, priority=0):
        super().__init__(model, name, "open", reference_station, priority)
        self.distribution = distribution

        # brutto, da rivedere
        self.set_attributes(
            {**self._attributes, **{"referenceSource": self.reference_station.name}})
        self.model.userclasses.append(self)
        # add random source to reference station # openclass? boh
        # if not hasattr(reference_station, "random_source"): VA IN CIMA
        if isinstance(reference_station, Source):
            reference_station.random_source.add_servicestrategy_entry(
                self, distribution)

# da vedere


class ClosedClass(_UserClass):
    def __init__(self, model, name, reference_station, customers, priority=0):
        super().__init__(model, name, "closed", reference_station, priority)
        self.customers = customers

        self.model.userclasses.append(self)
