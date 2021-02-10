class _XmlNode():
    def __init__(self, _tag, _children=None):
        self._tag = _tag
        if _children:  # dict mi va bene?
            assert isinstance(_children, list), "_children is not a list"
            self._children = _children
        else:
            self._children = []
        self._attributes = {}
        self._element = None

    def add_child(self, obj):
        self._children.append(obj)
