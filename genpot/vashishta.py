import re
import math
from .forcefield import ForceField

class Vashishta(ForceField):
    def __init__(self, base=None, **kwargs):
        super().__init__(base=base, **kwargs)
        # nested list defining how parameters should be distributed
        # through multiple lines, ordering should NOT be modified
        self.suffices = [["H", "eta", "Zi", "Zj", "r1s", "D", "r4s"],
                         ["W", "rc", "B", "xi", "r0", "C", "cos(theta)"]]
        #self.base = base
        #if base is not None:
        #    self._collect_params()

    def scale(self, scalefactor, mod_msg=True):
        if mod_msg and not self.modified:
            self.header += "# NB: THE PARAMETERS HAVE BEEN MODIFIED. POTENTIAL SCALED BY %.2f\n#\n" % scalefactor
            self.modified = True
        for pair in self.params:
            for var in ["H", "D", "W", "B"]:
                self.params[pair][var] *= scalefactor
            for var in ["Zi", "Zj"]:
                self.params[pair][var] *= math.sqrt(scalefactor)
        return

    def __repr__(self):
        return "vashishta"

    def update_params(self, params={}, mod_msg=True):
        """Updates the parameter dictionary
        """
        if mod_msg and not self.modified:
            self.header += "# NB: THE PARAMETERS HAVE BEEN MODIFIED\n#\n"
            self.modified = True
        for groups, parameters in params.items():
            groups = groups.split(",")
            for group in groups:
                if group == "global":
                    map = {0: 'i', 1: 'j'}
                    for key, value in parameters.items():
                        if key.startswith("Z_"):
                            this = key.split("_")[-1]
                            charge_this = value
                            for atom, multi in self.multiplicity.items():
                                if atom == this:
                                    multi_this = multi
                                else:
                                    other = atom
                                    multi_other = multi
                            charge_other = - charge_this * multi_this / multi_other
                            for group in self.params.keys():
                                group_split = re.findall('[A-Z][^A-Z]*', group)
                                for i, atom in enumerate(group_split[:2]):
                                    n = map[i]
                                    if atom == this:
                                        self.params[group][f"Z{n}"] = charge_this
                                    elif atom == other:
                                        self.params[group][f"Z{n}"] = charge_other
                        if key.startswith("sigma_"):
                            this = key.split("_")[-1]
                            for group in self.params.keys():
                                assert 'A' in self.params[group], "'A' does not exist, add it without the 'global' group"
                                assert 'sigmai' in self.params[group], "'sigmai' does not exist, add it without the 'global' group"
                                assert 'sigmaj' in self.params[group], "'sigmaj' does not exist, add it without the 'global' group"
                                group_dict = self.params[group]
                                group_split = re.findall('[A-Z][^A-Z]*', group)
                                for i, atom in enumerate(group_split[:2]):
                                    if atom == this:
                                        group_dict[f"sigma{map[i]}"] = value
                                group_dict["H"] = group_dict["A"] * (group_dict["sigmai"]+group_dict["sigmaj"])**group_dict["eta"]
                                self.params[group] = group_dict
                        if key.startswith("alpha_"):
                            this = key.split("_")[-1]
                            for group in self.params.keys():
                                assert 'alphai' in self.params[group], "'alphai' does not exist, add it without the 'global' group"
                                assert 'alphaj' in self.params[group], "'alphaj' does not exist, add it without the 'global' group"
                                group_dict = self.params[group]
                                group_split = re.findall('[A-Z][^A-Z]*', group)
                                for i, atom in enumerate(group_split[:2]):
                                    if atom == this:
                                        group_dict[f"alpha{map[i]}"] = value
                                group_dict["D"] = 0.5 * (group_dict["alphai"]*group_dict["Zj"]**2+group_dict["alphaj"]*group_dict["Zi"]**2)
                                self.params[group] = group_dict

                elif group == "all":
                    for key, value in parameters.items():
                        for group in self.params.keys():
                            self.params[group][key] = value
                else:
                    for parameter, value in parameters.items():
                        self.params[group][parameter] = value
