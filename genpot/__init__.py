import os
import re
import shutil
import importlib


class Potential:
    def __init__(self):
        pass

    def __repr__(self):
        return ""

    def list_params(self):
        """List all available parameterizations.
        """
        dirname = os.path.dirname(__file__)
        path = os.path.join(dirname, f"param/{self.__repr__()}")
        files = os.listdir(path)
        files = [os.path.splitext(file)[0] for file in files]
        print(', '.join(files))
        return files

    def __call__(self):
        """Generate parameter file
        """
        pass


class StillingerWeber(Potential):
    def __init__(self):
        pass

    def __repr__(self):
        return "sw"


class Vashishta(Potential):
    def __init__(self):
        pass

    def __repr__(self):
        return "vashishta"

    def set_params(self, base):
        """Set parameter set
        """
        this_dir, this_filename = os.path.split(__file__)
        rel_path = os.path.relpath(this_dir)
        print(rel_path)
        param_path = f"param.{self.__repr__()}.{base}"
        module = importlib.import_module(param_path, package=None)
        params, molecule = module.params, module.molecule
        self.molecule = re.findall('[A-Z][^A-Z]*', molecule)
        self.multiplicity = {}
        for atom in self.molecule:
            cnt = self.molecule.count(atom)
            self.multiplicity[atom] = cnt
        self.params = params

    def update_params(self, params={}):
        """Updates the parameter dictionary
        """
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
        params_line1 = ["H", "eta", "Zi", "Zj", "r1s", "D", "r4s"]
        params_line2 = ["W", "rc", "B", "xi", "r0", "C", "cos(theta)"]
        string_line1 = self._ordered_string(params, params_line1, prefix_list)
        string_line2 = self._ordered_string(params, params_line2, 3 * [''])

        with open(filename, 'a') as file:
            file.write("\n")
            file.write(string_line1)
            file.write(string_line2)

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
        header_filename = os.path.join(this_dir, "data/header.vashishta")

        shutil.copyfile(header_filename, filename)

        # Add parameters to file
        for group, params in self.params.items():
            self.append_type_to_file(group, params, filename)
