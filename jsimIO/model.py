from .defaults import *
from .xmlnode_superclass import *


class Model(XmlNode):
    def __init__(self, name, options=Default.ModelOptions):
        self._tag = "sim"
        self.options = options


class ClosedModel(Model):
    pass


class OpenModel(Model):
    pass
