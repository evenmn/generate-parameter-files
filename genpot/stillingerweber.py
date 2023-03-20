from .forcefield import ForceField

class StillingerWeber(ForceField):
    def __init__(self, base=None, **kwargs):
        super().__init__(base=base, **kwargs)
        # nested list defining how parameters should be distributed
        # through multiple lines, ordering should NOT be modified
        self.suffices = [["epsilon", "sigma", "a", "lambda", "gamma", "cos(theta)"],
                         ["A", "B", "p", "q", "tol"]]

        # define scaling factors
        self.scaling_factors = {'A': 'lin', 'lambda': 'lin'}


    def __repr__(self):
        return "sw"
