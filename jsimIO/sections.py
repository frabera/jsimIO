from .xmlnode_superclass import _XmlNode
# from .userclasses import _UserClass


class _Section(_XmlNode):
    def __init__(self, className):
        super().__init__("section")
        self.className = className
        self.set_attributes(self.get_classattributes_asdict())


#  STATION
class _Queue(_Section):  # is a section
    def __init__(self, scheduling_strategy, buffer_size, drop_strategy):
        super().__init__("Queue")
        self.scheduling_strategy = scheduling_strategy
        val = _XmlNode("value", text=buffer_size)
        self.add_child(_XmlNode("parameter", attributes={
                       "classPath": "java.lang.Integer", "name": "size"}, children=[val]))
        # self.add_child(_XmlNode)


class _Server(_Section):
    def __init__(self, service_strategy=None):
        super().__init__("Server")
        self.service_strategy = service_strategy


class _Router(_Section):
    def __init__(self, routing_strategy=None):
        super().__init__("Router")
        self.routing_strategy = routing_strategy


#  SOURCE
# RandomSource
# ServiceTunnel
class _ServiceTunnel(_Section):
    def __init__(self):
        super().__init__("ServiceTunnel")
# Router

#  SINK

# TODO Drop Strategies
