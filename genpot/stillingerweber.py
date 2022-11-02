from .forcefield import ForceField

class StillingerWeber(ForceField):
    def __init__(self, base=None, **kwargs):
        super().__init__(base=base, **kwargs)
        # nested list defining how parameters should be distributed
        # through multiple lines, ordering should NOT be modified
        self.suffices = [["epsilon", "sigma", "a", "lambda", "gamma", "cos(theta)"],
                         ["A", "B", "p", "q", "tol"]]
        #self.base = base
        #if base is not None:
        #    self._collect_params()

    def __repr__(self):
        return "sw"
