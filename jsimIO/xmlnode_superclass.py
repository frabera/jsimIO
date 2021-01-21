class XmlNode():
    def __init__(self, _tag, _children=None):
        self._tag = _tag
        if _children:  # dict mi va bene?
            assert isinstance(_children, list), "_children is not a list"
            self._children = _children
        else:
            self._children = []
