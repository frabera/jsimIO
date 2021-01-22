from .defaults import *
from .xmlnode_superclass import *


class Model(XmlNode):
    def __init__(self, name, options=Default.ModelOptions):
        self.options = options
        super().__init__("sim")
