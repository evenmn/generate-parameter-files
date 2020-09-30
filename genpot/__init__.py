import os
import re
import shutil
import datetime
import importlib


class Potential:
    def __init__(self, base=None):
        self.base = base
        if base is not None:
            self._collect_params()

    def __repr__(self):
        return ""

    def _write_header(self):
        package_name = "genpot"
        url = "http://www.github.com/evenmn/generate-parameter-files"
        cont = "Even M. Nordhagen"
        email = "evenmn@fys.uio.no"
        today = datetime.datetime.today()

        string = f"# THIS PARAMETER FILE WAS GENERATED USING {package_name} \n#\n"
        string += f"# URL: {url}\n"
        string += f"# CONTRIBUTOR: {cont}, {email}\n#\n"
        string += f"# DATE: {today:%B %d, %Y}\n"
        string += f"# CITATION: {self.citation}\n#\n"
        return string

    def list_params(self):
        """List all available parameterizations.
        """
        dirname = os.path.dirname(__file__)
        path = os.path.join(dirname, f"param/{self.__repr__()}")
        files = os.listdir(path)
        files = list(filter(lambda s: not s.startswith('__'), files))
        files = [os.path.splitext(file)[0] for file in files]
        print(', '.join(files))
        return files

    def set_params(self, base):
        """Set parameter set
        """
        self.base = base
        self._collect_params()

    def _collect_params(self):
        """collect information about base set
        """
        if self.base is None:
            raise TypeError("Base parameterization is not given!!")
        param_path = f"genpot.param.{self.__repr__()}.{self.base}"
        pm = importlib.import_module(param_path, package=None)
        self.params, molecule, self.citation = pm.params, pm.molecule, pm.citation
        # find multiplicity of atoms in molecule
        self.molecule = re.findall('[A-Z][^A-Z]*', molecule)
        self.multiplicity = {}
        for atom in self.molecule:
            cnt = self.molecule.count(atom)
            self.multiplicity[atom] = cnt
        self.header = self._write_header()

    @staticmethod
    def _ordered_string(params, param_suffices, param_list):
        """Returning an ordered list of all the parameter values

        :type params: dict
        :param params: dictionary with all parameters
        :type param_suffices: list of str
        :param param_suffices: correctly ordered list of all parameter suffices
        :type param_list: list
        :param param_list: initial list to append parameters to
        """
        string = ""
        for atom in param_list:
            string += f"{atom:<5}"
        for param in param_suffices:
            number = round(params[param], 6)
            string += f" {number:>10}"
        return string + "\n"

    def append_type_to_file(self, group, params, filename):
        """Append the actual parameter values to the parameter file.

        :type group: str
        :param group: group (e.g. "SiSiSi")
        :type params: dict
        :param params: dictionary with all parameters
        :type filename: str
        :param filename: parameter filename
        """
        # Split group
        prefix_list = re.findall('[A-Z][^A-Z]*', group)
        with open(filename, 'a') as f:
            f.write("\n")
            for i, suffix_list in enumerate(self.suffices):
                if i == 0:
                    string = self._ordered_string(params, suffix_list, prefix_list)
                else:
                    string = self._ordered_string(params, suffix_list, 3 * [''])
                f.write(string)

    def update_params(self, params={}):
        """Updates the parameter dictionary
        """
        self.header += "# NB: THE PARAMETERS HAVE BEEN MODIFIED\n#\n"
        for groups, parameters in params.items():
            groups = groups.split(",")
            for group in groups:
                if group == "global":
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
                            charge_map = {0: 'i', 1: 'j'}
                            for group in self.params.keys():
                                group_split = re.findall('[A-Z][^A-Z]*', group)
                                for i, atom in enumerate(group_split[:2]):
                                    n = charge_map[i]
                                    if atom == this:
                                        self.params[group][f"Z{n}"] = charge_this
                                    elif atom == other:
                                        self.params[group][f"Z{n}"] = charge_other
                elif group == "all":
                    for key, value in parameters.items():
                        for group in self.params.keys():
                            self.params[group][key] = value
                else:
                    for parameter, value in parameters.items():
                        self.params[group][parameter] = value

    def __call__(self, filename="dest.vashishta"):
        """Generates input parameter file for the potential. The default
        parameters are the ones specified in Wang et al., so parameters
        that are not specified will fall back on these default parameters.

        :param substance: substance to simulate
        :type substance: str
        :param filename: filename of parameter file
        :type filename: str
        :param params: dictionary of parameters that should be changed
        :type params: dict
        """
        # Make new parameter file
        this_dir, this_filename = os.path.split(__file__)
        header_filename = os.path.join(this_dir, f"data/header.{self.__repr__()}")

        shutil.copyfile(header_filename, filename)
        with open(filename, 'r+') as f:
            content = f.read()
            f.seek(0, 0)
            f.write(self.header.rstrip('\r\n') + '\n' + content)
            for suffix_list in self.suffices:
                f.write("#" + 11 * " " + ", ".join(suffix_list) + "\n")

        # Add parameters to file
        for group, params in self.params.items():
            self.append_type_to_file(group, params, filename)
        print(f"New parameter file '{filename}' successfully generated!")


class StillingerWeber(Potential):
    def __init__(self, base=None):
        # nested list defining how parameters should be distributed
        # through multiple lines, ordering should NOT be modified
        self.suffices = [["epsilon", "sigma", "a", "lambda", "gamma", "cos(theta)"],
                         ["A", "B", "p", "q", "tol"]]
        self.base = base
        if base is not None:
            self._collect_params()

    def __repr__(self):
        return "sw"


class Vashishta(Potential):
    def __init__(self, base=None):
        # nested list defining how parameters should be distributed
        # through multiple lines, ordering should NOT be modified
        self.suffices = [["H", "eta", "Zi", "Zj", "r1s", "D", "r4s"],
                         ["W", "rc", "B", "xi", "r0", "C", "cos(theta)"]]
        self.base = base
        if base is not None:
            self._collect_params()

    def __repr__(self):
        return "vashishta"


class TIP4P(Potential):
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

    def __call__(self, filename="params.in"):
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
        print(f"New parameter file '{filename}' successfully generated!")
