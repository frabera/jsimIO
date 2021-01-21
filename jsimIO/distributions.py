from .xmlnode_superclass import *


class Distribution(XmlNode):
    pass


class Exp(Distribution):
    def __init__(self, lambda_):
        self.lambda_ = lambda_

    def fit_mean(mean):  # cls method?
        assert mean, "Error, mean can not be equal to zero."
        return Exp(1 / mean)


class HyperExp(Distribution):
    pass
