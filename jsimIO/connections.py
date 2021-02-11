import lxml.etree as ET

from .xmlnode_superclass import _XmlNode


class _Connection(_XmlNode):
    def __init__(self, source, target):
        super().__init__("connection")
        self.source = source
        self.target = target
        self._attributes = {"source": source, "target": target}
        self._element = ET.Element(self._tag, self._attributes)
