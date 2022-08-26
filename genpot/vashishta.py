import math
from .forcefield import ForceField

class Vashishta(ForceField):
    def __init__(self, base=None):
        # nested list defining how parameters should be distributed
        # through multiple lines, ordering should NOT be modified
        self.suffices = [["H", "eta", "Zi", "Zj", "r1s", "D", "r4s"],
                         ["W", "rc", "B", "xi", "r0", "C", "cos(theta)"]]
        self.base = base
        if base is not None:
            self._collect_params()

    def scale(self, scalefactor):
        self.header += "# NB: THE PARAMETERS HAVE BEEN MODIFIED. POTENTIAL SCALED BY %.2f\n#\n" % scalefactor
        for pair in self.params:
            for var in ["H", "D", "W", "B"]:
                self.params[pair][var] *= scalefactor
            for var in ["Zi", "Zj"]:
                self.params[pair][var] *= math.sqrt(scalefactor)
        return

    def __repr__(self):
        return "vashishta"
