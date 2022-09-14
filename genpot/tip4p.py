from .forcefield import ForceField

class TIP4P(ForceField):
    def __init__(self, base=None):
        self.sufficies = ["Z_H", "Z_O", "r0", "theta", "OM", "epsilon",
                          "sigma", "r4s"]
        self.mass_H = 1.00794
        self.mass_O = 15.9994
        self.base = base
        if base is not None:
            self._collect_params()

    def __repr__(self):
        return "tip4p"

    def update_params(self, params={}):
        """Updates the parameter dictionary
        """
        for key, value in params.items():
            self.params[key] = value
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
                self.params[f"Z_{other}"] = charge_other

    def write(self, filename="params.in", success_msg=True):
        # Collect base parameters if not already done
        if 'params' not in globals():
            self._collect_params()
        with open(filename, 'w') as f:
            f.write(f"mass 1 {self.mass_H}\n")
            f.write(f"mass 2 {self.mass_O}\n\n")

            f.write(f"set type 1 charge {self.params['Z_H']}\n")
            f.write(f"set type 2 charge {self.params['Z_O']}\n\n")

            f.write(f"pair_style lj/cut/tip4p/long 2 1 1 1 {self.params['OM']} {self.params['r4s']}\n")
            f.write("pair_modify tail yes\n")
            f.write("kspace_style pppm/tip4p 1.0e-5\n\n")

            f.write("pair_coeff 1 1 0.0 0.0\n")
            f.write("pair_coeff 1 2 0.0 0.0\n")
            f.write(f"pair_coeff 2 2 {self.params['epsilon']} {self.params['sigma']}\n\n")

            f.write("bond_style harmonic\n")
            f.write(f"bond_coeff 1 0.0 {self.params['r0']}\n\n")

            f.write("angle_style harmonic\n")
            f.write(f"angle_coeff 1 0.0 {self.params['theta']}\n")
        if success_msg:
            print(f"New parameter file '{filename}' successfully generated!")
