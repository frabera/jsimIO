import lxml.etree as ET
from .xmlnode_superclass import _XmlNode, _SubParameter


class Disable(_SubParameter):
    def __init__(self):
        super().__init__("jmt.engine.NetStrategies.ServiceStrategies.DisabledServiceTimeStrategy",
                         "DisabledServiceTimeStrategy")


class _Distribution(_SubParameter):
    def __init__(self):
        super().__init__("jmt.engine.NetStrategies.ServiceStrategies.ServiceTimeStrategy",
                         "ServiceTimeStrategy")


class Dist:

    class Determ(_Distribution):
        def __init__(self, k):
            super().__init__()
            assert k, "k cannot be equal to zero."
            self.k = k

            self.add_child(
                _SubParameter(
                    "jmt.engine.random.DeterministicDistr", "Deterministic"))
            self.add_child(
                _SubParameter(
                    "jmt.engine.random.DeterministicDistrPar", "distrPar", children=[
                        _SubParameter(
                            "java.lang.Double", "t", value=str(float(self.k))
                        )
                    ]
                )
            )

    class Exp(_Distribution):
        def __init__(self, lambda_):
            super().__init__()
            self.lambda_ = lambda_
            self.add_child(
                _SubParameter(
                    "jmt.engine.random.Exponential", "Exponential"))
            self.add_child(
                _SubParameter(
                    "jmt.engine.random.ExponentialPar", "distrPar", children=[
                        _SubParameter(
                            "java.lang.Double", "lambda", value=str(float(self.lambda_))
                        )
                    ]
                )
            )

        @classmethod
        def fit_mean(cls, mean):  # cls method?
            assert mean, "Mean cannot be equal to zero."
            return cls(1 / mean)

    class HyperExp(_Distribution):
        def __init__(self, p, lambda_1, lambda_2):
            super().__init__()
            assert lambda_1 and lambda_2, "Lambdas cannot be equal to zero"
            self.p = p
            self.lambda_1 = lambda_1
            self.lambda_2 = lambda_2

            self.add_child(_SubParameter(
                "jmt.engine.random.HyperExp",
                "Hyperexponential"
            ))
            self.add_child(_SubParameter(
                "jmt.engine.random.HyperExpPar",
                "distrPar",
                children=[
                    _SubParameter("java.lang.Double", "p", value=self.p),
                    _SubParameter("java.lang.Double", "lambda1",
                                  value=self.lambda_1),
                    _SubParameter("java.lang.Double", "lambda2",
                                  value=self.lambda_2)
                ]
            ))

    class Uniform(_Distribution):
        def __init__(self, min_, max_):
            super().__init__()
            assert max_ > min_, "Max must be greater than min"
            self.max_ = max_
            self.min_ = min_

            self.add_child(_SubParameter(
                "jmt.engine.random.Uniform",
                "Uniform"
            ))
            self.add_child(_SubParameter(
                "jmt.engine.random.UniformPar",
                "distrPar",
                children=[
                    _SubParameter("java.lang.Double", "min", value=self.min_),
                    _SubParameter("java.lang.Double", "max", value=self.max_)
                ]
            ))

    class Normal(_Distribution):
        def __init__(self, mean, stdev):
            super().__init__()
            assert stdev, "Standard deviation cannot be equal to zero"
            self.mean = mean
            self.stdev = stdev

            self.add_child(_SubParameter(
                "jmt.engine.random.Normal",
                "Normal"
            ))
            self.add_child(_SubParameter(
                "jmt.engine.random.NormalPar",
                "distrPar",
                children=[
                    _SubParameter("java.lang.Double", "mean", value=self.mean),
                    _SubParameter("java.lang.Double",
                                  "standardDeviation", value=self.stdev)
                ]
            ))

    class Gamma(_Distribution):
        def __init__(self, alpha, theta):
            super().__init__()
            assert alpha and theta, "Parameters cannot be equal to zero."
            self.alpha = alpha
            self.theta = theta

            self.add_child(_SubParameter(
                "jmt.engine.random.GammaDistr",
                "Gamma"
            ))
            self.add_child(_SubParameter(
                "jmt.engine.random.GammaDistrPar",
                "distrPar",
                children=[
                    _SubParameter("java.lang.Double",
                                  "alpha", value=self.alpha),
                    _SubParameter("java.lang.Double", "beta", value=self.theta)
                ]
            ))

    class Erlang(_Distribution):
        def __init__(self, lambda_, k):
            super().__init__()
            assert lambda_ and k, "Parameters cannot be equal to zero."
            self.lambda_ = lambda_
            self.k = k

            self.add_child(_SubParameter(
                "jmt.engine.random.Erlang",
                "Erlang"
            ))
            self.add_child(_SubParameter(
                "jmt.engine.random.ErlangPar",
                "distrPar",
                children=[
                    _SubParameter("java.lang.Double", "alpha",
                                  value=self.lambda_),
                    _SubParameter("java.lang.Double", "r", value=self.k)
                ]
            ))

    class Coxian(_Distribution):
        def __init__(self, lambda_0, lambda_1, p0):
            super().__init__()
            assert lambda_0 and lambda_1, "Lambdas cannot be equal to zero"
            self.lambda_0 = lambda_0
            self.lambda_1 = lambda_1
            self.p0 = p0

            self.add_child(_SubParameter(
                "jmt.engine.random.CoxianDistr",
                "Coxian"
            ))
            self.add_child(_SubParameter(
                "jmt.engine.random.CoxianPar",
                "distrPar",
                children=[
                    _SubParameter("java.lang.Double", "lambda0",
                                  value=self.lambda_0),
                    _SubParameter("java.lang.Double", "lambda1",
                                  value=self.lambda_1),
                    _SubParameter("java.lang.Double", "phi0", value=self.p0)
                ]
            ))

    class Pareto(_Distribution):
        def __init__(self, alpha, k):
            super().__init__()
            assert alpha and k, "Parameters cannot be zero"
            self.alpha = alpha
            self.k = k

            self.add_child(_SubParameter(
                "jmt.engine.random.Pareto",
                "Pareto"
            ))
            self.add_child(_SubParameter(
                "jmt.engine.random.ParetoPar",
                "distrPar",
                children=[
                    _SubParameter("java.lang.Double", "alpha",
                                  value=self.alpha),
                    _SubParameter("java.lang.Double", "k", value=self.k)
                ]
            ))

    class PhaseType(_Distribution):
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

    class BurstMMPP2(_Distribution):
        def __init__(self, lambda_0, lambda_1, sigma_0, sigma_1):
            super().__init__()
            assert lambda_0 and lambda_1 and sigma_0 \
                and sigma_1, "Parameters cannot be equal to zero"
            self.lambda_0 = lambda_0
            self.lambda_1 = lambda_1
            self.sigma_0 = sigma_0
            self.sigma_1 = sigma_1

    class BurstMAP(_Distribution):
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

    class BurstGeneral(_Distribution):
        def __init__(self, interval_distrib_A, value_distrib_A,
                     interval_distrib_B, value_distrib_B,
                     probability_A=None, probability_B=None,
                     round_robin=False):
            super().__init__()
            assert probability_A or probability_B or round_robin, \
                "Either insert values for Probability of A and B or set round_robin to True"
            assert isinstance(interval_distrib_A, _Distribution) and \
                isinstance(interval_distrib_B, _Distribution) and \
                isinstance(value_distrib_A, _Distribution) and \
                isinstance(value_distrib_B, _Distribution), \
                "Insert Distribution class parameters"
            self.round_robin = round_robin
            self.interval_distrib_A = interval_distrib_A
            self.value_distrib_A = value_distrib_A
            self.interval_distrib_B = interval_distrib_B
            self.value_distrib_B = value_distrib_B
