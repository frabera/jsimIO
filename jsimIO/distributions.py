import lxml.etree as ET
from .xmlnode_superclass import *


class Distribution(XmlNode):
    def __init__(self):
        pass


class Determ(Distribution):
    def __init__(self, k):
        super().__init__()
        assert k, "k cannot be equal to zero."
        self.k = k

    def fit_mean(mean):  # cls method?
        assert mean, "Mean cannot be equal to zero."
        return Determ(mean)

    def get_element(self):
        pass


class Exp(Distribution):
    def __init__(self, lambda_):
        super().__init__()
        self.lambda_ = lambda_

    def fit_mean(mean):  # cls method?
        assert mean, "Mean cannot be equal to zero."
        return Exp(1 / mean)

    def get_elements_list(self):
        elements = []
        elements.append(ET.Element("subParameter",
                                   classPath="jmt.engine.random.Exponential",
                                   name="Exponential"))
        el2 = ET.Element("subParameter",
                         classPath="jmt.engine.random.ExponentialPar",
                         name="distrPar")
        elements.append(el2)
        el2a = ET.SubElement(el2, "subParameter",
                             classPath="java.lang.Double",
                             name="lambda")
        el2a1 = ET.SubElement(el2a, "value")
        el2a1.text = str(float(self.lambda_))
        return elements


class HyperExp(Distribution):
    def __init__(self, p, lambda_1, lambda_2):
        super().__init__()
        assert lambda_1 and lambda_2, "Lambdas cannot be equal to zero"
        self.p = p
        self.lambda_1 = lambda_1
        self.lambda_2 = lambda_2


class Uniform(Distribution):
    def __init__(self, min_, max_):
        super().__init__()
        assert max_ > min_, "Max must be greater than min"
        self.max_ = max_
        self.min_ = min_


class Normal(Distribution):
    def __init__(self, mean, stdev):
        super().__init__()
        assert stdev, "Standard deviation cannot be equal to zero"
        self.mean = mean
        self.stdev = stdev


class Gamma(Distribution):
    def __init__(self, alpha, theta):
        super().__init__()
        assert alpha and theta, "Parameters cannot be equal to zero."
        self.alpha = alpha
        self.theta = theta


class Erlang(Distribution):
    def __init__(self, lambda_, k):
        super().__init__()
        assert lambda_ and k, "Parameters cannot be equal to zero."
        self.lambda_ = lambda_
        self.k = k


class Coxian(Distribution):
    def __init__(self, lambda_0, lambda_1, p0):
        super().__init__()
        assert lambda_0 and lambda_1, "Lambdas cannot be equal to zero"
        self.lambda_0 = lambda_0
        self.lambda_1 = lambda_1
        self.p0 = p0


class Pareto(Distribution):
    def __init__(self, alpha, k):
        super().__init__()
        assert alpha and k, "Parameters cannot be zero"
        self.alpha = alpha
        self.k = k


class PhaseType(Distribution):
    def __init__(self, initial_prob_vector, transition_matrix):
        super().__init__()
        assert len(transition_matrix) == len(
            transition_matrix[0]), "Transition matrix must be squared"
        # not checking all the rows
        assert len(initial_prob_vector) == len(
            transition_matrix), "Vector dimension different from matrix"
        self.initial_prob_vector = initial_prob_vector
        self.transition_matrix = transition_matrix
        self.dimension = len(initial_prob_vector)


class BurstMMPP2(Distribution):
    def __init__(self, lambda_0, lambda_1, sigma_0, sigma_1):
        super().__init__()
        assert lambda_0 and lambda_1 and sigma_0 \
            and sigma_1, "Parameters cannot be equal to zero"
        self.lambda_0 = lambda_0
        self.lambda_1 = lambda_1
        self.sigma_0 = sigma_0
        self.sigma_1 = sigma_1


class BurstMAP(Distribution):
    def __init__(self, hidden_trans_matrix, observable_trans_matrix):
        super().__init__()
        assert len(hidden_trans_matrix) == len(
            hidden_trans_matrix[0]), "Transition matrix must be squared"
        assert len(observable_trans_matrix) == len(
            observable_trans_matrix[0]), "Transition matrix must be squared"
        # not checking all the rows
        assert len(observable_trans_matrix) == len(
            hidden_trans_matrix), "Matrix dimensions must be equal"
        self.hidden_trans_matrix = hidden_trans_matrix
        self.observable_trans_matrix = observable_trans_matrix
        self.number_of_states = len(hidden_trans_matrix)


class BurstGeneral(Distribution):
    def __init__(self, interval_distrib_A, value_distrib_A,
                 interval_distrib_B, value_distrib_B,
                 probability_A=None, probability_B=None,
                 round_robin=False):
        super().__init__()
        assert probability_A or probability_B or round_robin, \
            "Either insert values for Probability of A and B or set round_robin to True"
        assert isinstance(interval_distrib_A, Distribution) and \
            isinstance(interval_distrib_B, Distribution) and \
            isinstance(value_distrib_A, Distribution) and \
            isinstance(value_distrib_B, Distribution),\
            "Insert Distribution class parameters"
        self.round_robin = round_robin
        self.interval_distrib_A = interval_distrib_A
        self.value_distrib_A = value_distrib_A
        self.interval_distrib_B = interval_distrib_B
        self.value_distrib_B = value_distrib_B


# Missing: Burst(general)
