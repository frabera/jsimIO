from .xmlnode_superclass import *


class UserClass(XmlNode):
    def __init__(self, name, priority):
        self.name = name
        self.priority = priority

        self.tag = "userClass"


class ClosedClass(UserClass):
    def __init__(self, name, customers, priority=0):
        super().__init__(name, priority)
        self.customers = customers
        self.type = "closed"


class OpenClass(UserClass):
    def __init__(self, name, priority=0):
        super().__init__(name, priority)
        self.type = "open"
