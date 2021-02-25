import lxml.etree as ET


class _XmlNode():
    def __init__(self, tag, children=None, text=None, attributes={}):
        self._tag = tag
        self._text = text
        self._children = []
        self._element = ET.Element(self._tag, attrib=attributes)
        if self._text:
            self._element.text = str(self._text)
        if children:  # dict mi va bene?
            assert isinstance(children, list), "_children is not a list"
            for child in children:
                self.add_child(child)
        self._attributes = {}
        # ! MACELLI CON ATTRIBUTES!
        # self._attributes è superfluo

        self.set_attributes(attributes)

    def add_child(self, xmlnode_instance):
        self._children.append(xmlnode_instance)
        self._element.append(xmlnode_instance._element)
        return xmlnode_instance

    def get_classattributes_asdict(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith(("_", "model"))}

    def get_child(self, id):
        return self._children[id]

    def get_children_xmlelements(self):
        return [child._element for child in self._children]
        # corrisponde a esplorare l'albero xml?
        # conviene accedere a _children o a i figli di _element?

    def current_attributes_to_element(self):
        self._element.attrib.update(self.get_classattributes_asdict())
        self._attributes.update(self.get_classattributes_asdict())

    def set_attributes(self, attr_dict):
        attr_dict_cleaned = {str(k): str(v)
                             for k, v in attr_dict.items()}  # Converto in stringhe
        self._attributes.update(attr_dict_cleaned)
        self._element.attrib.update(attr_dict_cleaned)

    # genera elem xml da attributi classe, potrebbe servire se genero xml alla fine
    def create_element(self):
        pass
